from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime
from sqlalchemy.ext.asyncio import  AsyncSession
from src.models import Website, Question, QuestionOption




# Create Functions
async def create_website(db: AsyncSession, url: str, content: Optional[str] = None) -> Website:
    """Create a new website entry."""
    website = Website(url=url, content=content)
    db.add(website)
    await db.commit()
    await db.refresh(website)
    return website

async def create_question(db: AsyncSession, website_id: int, text: str) -> Question:
    """Create a new question for a website."""
    question = Question(website_id=website_id, text=text)
    db.add(question)
    await db.commit()
    await db.refresh(question)
    return question

async def create_question_option(db: AsyncSession, question_id: int, text: str) -> QuestionOption:
    """Create a new option for a question."""
    option = QuestionOption(question_id=question_id, text=text)
    db.add(option)
    await db.commit()
    await db.refresh(option)
    return option


async def bulk_create_questions_for_website(
    db: AsyncSession,
    website_id: int,
    questions_data: List[Dict[str, Any]]
) -> List[Question]:
    """
    Bulk create questions with their options for a specific website.
    
    Args:
        db: Database session
        website_id: ID of the website these questions belong to
        questions_data: List of dictionaries with format:
            [
                {
                    "question": "What is your favorite color?",
                    "options": ["Red", "Blue", "Green"]
                },
                {
                    "question": "What is your age group?",
                    "options": ["18-24", "25-34", "35+"]
                }
            ]
    
    Returns:
        List of created Question objects with their options loaded
    """
    # First verify the website exists
    website = await db.execute(
        select(Website).where(Website.id == website_id)
    )
    if not website.scalar_one_or_none():
        raise ValueError(f"Website with ID {website_id} not found")

    # Create all questions first
    questions = [
        Question(
            website_id=website_id,
            text=q_data['question']
        )
        for q_data in questions_data
    ]
    db.add_all(questions)
    await db.flush()  # Flush to get question IDs without committing

    # Create all options for all questions
    all_options = []
    for question, q_data in zip(questions, questions_data):
        options = [
            QuestionOption(
                question_id=question.id,
                text=option_text
            )
            for option_text in q_data['options']
        ]
        all_options.extend(options)

    if all_options:
        db.add_all(all_options)
    
    await db.commit()

    # Refresh questions to get their options
    for question in questions:
        await db.refresh(question, ['options'])
    
    return questions

# Read Functions
async def get_website_by_id(db: AsyncSession, website_id: int) -> Optional[Website]:
    """Get a website by ID with all related questions and options."""
    query = select(Website).where(Website.id == website_id).options(
        selectinload(Website.questions).selectinload(Question.options)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_website_by_url(db: AsyncSession, url: str) -> Optional[Website]:
    """Get a website by URL with all related questions and options."""
    query = select(Website).where(Website.url == url).options(
        selectinload(Website.questions).selectinload(Question.options)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_all_websites(db) -> List[Website]:
    """Get all websites (without loading relationships)."""
    query = select(Website)
    result = await db.execute(query)
    return result.scalars().all()

async def get_question_by_id(db: AsyncSession, question_id: int) -> Optional[Question]:
    """Get a question by ID with all options."""
    query = select(Question).where(Question.id == question_id).options(
        selectinload(Question.options)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_questions_by_website_id(db: AsyncSession, website_id: int) -> List[Question]:
    """Get all questions for a specific website with their options."""
    query = select(Question).where(Question.website_id == website_id).options(
        selectinload(Question.options)
    )
    result = await db.execute(query)
    return result.scalars().all()

async def get_options_by_question_id(db: AsyncSession, question_id: int) -> List[QuestionOption]:
    """Get all options for a specific question."""
    query = select(QuestionOption).where(QuestionOption.question_id == question_id)
    result = await db.execute(query)
    return result.scalars().all()