import asyncio
from datetime import datetime
import os
import json
import time
import uuid
import redis
from flask import Flask, Response, request

from src.utils.utils import capture_screenshot, upload_to_s3
from src.utils.scraper import WebsiteScraper
from src.task import process_links_task
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
redis_client = redis.Redis(host='localhost', port=6379, db=0)


# Root route
@app.route("/")
async def index():
    return {"message": "Welcome to the Flask App"}


@app.route('/generate-content/', methods=['GET'])
async def generate_content():
    """Initial endpoint to start question generation"""
    # Generate session ID for this request
    url = request.args.get("url")
    
    if not url:
        return {"error": "No URL provided"}, 400
    
    scraper = WebsiteScraper(url)
    valid = scraper._is_valid_url(url)
    if not valid:
        return {"error": "Invalid URL provided"}, 400
    
    session_id = str(uuid.uuid4())
    
    links_cached = redis_client.get(f"{url}:links")
    
    if links_cached:
        process_links_task.delay(session_id, scraper)
        return {
            'session_id': session_id,
            'links': json.loads(links_cached)
        }
    
    await scraper.scrape_all()
    links = list(scraper.links) + [scraper.url]
    process_links_task.delay(session_id, scraper)
    
    if len(links) > 1: # Only cache when we see more than the original link
        redis_client.set(f"{url}:links", json.dumps(links))
        
    return {
        'session_id': session_id,
        'links': links
    }


@app.route("/preview-img/")
async def get_preview_image() -> dict:
    """Main function to get preview image URL for the given URL."""
    url = request.args.get("url")
    
    if not url:
        return {"error": "No URL provided"}, 400
    
    scraper = WebsiteScraper(url)
    valid = scraper._is_valid_url(url)
    if not valid:
        return {"error": "Invalid URL provided"}, 400
    
    img_cached = redis_client.get(f"{url}:img")
    if img_cached:
        return {"image": img_cached.decode('utf-8')}
    
    screenshot_path = await capture_screenshot(url)
    
    # Step 2: Define S3 bucket and object name
    bucket_name = os.getenv('AWS_BUCKET')
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    object_name = f"{timestamp}.png"
    
    # Step 3: Upload to S3 and get public URL
    image_url = upload_to_s3(screenshot_path, bucket_name, object_name)
    
    redis_client.set(f"{url}:img", image_url)
    return {
        'image': image_url
    }


@app.route('/stream/<session_id>')
def stream(session_id: str):
    """SSE endpoint for streaming question updates"""
    def generate():
        # Subscribe to Redis channel
        pubsub = redis_client.pubsub()
        pubsub.subscribe(f'questions:{session_id}')
        
        try:
            while True:
                message = pubsub.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    data = json.loads(message['data'])
                    print(data)
                    # Check if processing is complete
                    if data.get('status') == 'complete':
                        break
                    
                    yield f"data: {json.dumps(data)}\n\n"
                
                time.sleep(0.1)
                
        finally:
            pubsub.unsubscribe(f'questions:{session_id}')
            pubsub.close()
    
    return Response(
        generate(),
        mimetype='text/event-stream',
    )
    



if __name__ == "__main__":
    app.run(debug=True)
