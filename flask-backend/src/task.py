import asyncio
from datetime import datetime
import json
from celery import Celery
import redis.asyncio as async_redis

from src.crud import create_website, bulk_create_questions_for_website, get_questions_from_url
from src.db import db_session
from src.utils.llm import QuestionGenerator
from src.utils.utils import format_question_for_api
from typing import Dict, List, Optional
import json
import logging
from dataclasses import dataclass
from asgiref.sync import async_to_sync
from sqlalchemy.ext.asyncio import AsyncSession


logger = logging.getLogger(__name__)
celery = Celery(
    "task",
    broker='redis://localhost:6379/0',
    include=["src.task"]
)



@dataclass
class QuestionPayload:
    """Data structure for question response payload"""
    link: str
    questions: List[dict]

class ProcessingError(Exception):
    """Custom exception for processing errors"""
    

@celery.task
def process_links_task(
    session_id: str,
    scraped_info: dict,
):
    redis_client = async_redis.Redis(host='localhost', port=6379, db=0)
    async_to_sync(process_links)(session_id, scraped_info, redis_client)


async def process_links(
    session_id: str,
    scraped_info: dict,
    redis_client: async_redis.Redis
) -> None:
    """
    Processes website links to generate and publish questions.
    
    Args:
        session_id: Unique identifier for the processing session
        scraped_info: Dictionary of relevant info from scraped user's request
        redis_client: Redis client instance for caching and pub/sub
        question_generator: Instance of QuestionGenerator
    
    Raises:
        ProcessingError: If there's an error during processing
    """
    try:
        question_generator = QuestionGenerator(scraped_info)
        # Process main page
        await process_main_page(
            session_id=session_id,
            redis_client=redis_client,
            question_generator=question_generator
        )
        
        # Mark processing as complete
        await publish_completion_status(session_id, redis_client)
        
    except Exception as e:
        logger.error(f"Error processing links for session {session_id}: {str(e)}")
        await publish_error_status(session_id, redis_client, str(e))
        raise ProcessingError(f"Failed to process links: {str(e)}")

@db_session
async def process_main_page(
    db: AsyncSession,
    session_id: str,
    redis_client: async_redis.Redis,
    question_generator: QuestionGenerator
) -> None:
    """Processes the main page content and generates questions."""
    try:
        cached_questions = await get_cached_questions(redis_client, question_generator.url_info['url'])
        if cached_questions:
            questions = cached_questions
            await asyncio.sleep(1) # allow frontend to connect
        else:
            questions = await get_questions_from_url(question_generator.url_info['url'])
            if questions is None:
                questions = question_generator.generate_questions()
                if len(questions) > 0:
                    await cache_questions(redis_client, question_generator.url_info['url'], questions)
                    # Add to db
                    website = await create_website(db, question_generator.url_info['url'], question_generator.url_info['main_page_text'])
                    await bulk_create_questions_for_website(db, website.id, questions)
            else:
                questions = format_question_for_api(questions)
                
        await publish_questions(
            session_id=session_id,
            redis_client=redis_client,
            payload=QuestionPayload(link=question_generator.url_info['url'], questions=questions)
        )
    
    except Exception as e:
        logger.error(f"Error processing main page: {str(e)}")
        raise


async def get_cached_questions(
    redis_client: async_redis.Redis,
    url: str
) -> Optional[List[dict]]:
    """Retrieves cached questions for a given URL."""
    cached_data = await redis_client.get(f"{url}:questions")
    return json.loads(cached_data) if cached_data else None


async def cache_questions(
    redis_client: async_redis.Redis,
    url: str,
    questions: List[dict]
) -> None:
    """Caches questions for a given URL."""
    await redis_client.set(f"{url}:questions", json.dumps(questions))


async def publish_questions(
    session_id: str,
    redis_client: async_redis.Redis,
    payload: QuestionPayload
) -> None:
    """Publishes questions to the Redis channel."""
    await redis_client.publish(
        f'questions:{session_id}',
        json.dumps(payload.__dict__)
    )
    print("published")


async def publish_completion_status(
    session_id: str,
    redis_client: async_redis.Redis
) -> None:
    """Publishes completion status to the Redis channel."""
    await redis_client.publish(
        f'questions:{session_id}',
        json.dumps({'status': 'complete'})
    )


async def publish_error_status(
    session_id: str,
    redis_client: async_redis.Redis,
    error_message: str
) -> None:
    """Publishes error status to the Redis channel."""
    await redis_client.publish(
        f'questions:{session_id}',
        json.dumps({
            'status': 'error',
            'error': error_message
        })
    )



if __name__ == '__main__':
    redis_client = async_redis.Redis(host='localhost', port=6379, db=0)
    celery.worker_main(['worker', '--loglevel=info'])