# Website Analysis & Question Generation API

A sophisticated backend service that analyzes websites to generate personalized questionnaires for visitor categorization. The system scrapes website content, processes it using AI, and dynamically generates relevant multiple-choice questions.

## 🚀 Features

- **Website Content Analysis**: Scrapes and analyzes website content including sublinks
- **AI-Powered Question Generation**: Uses Google's Gemini AI for intelligent question formulation
- **Keyword Extraction**: Implements RAKE algorithm for key topic identification
- **Real-time Updates**: Server-Sent Events (SSE) for live question delivery
- **Website Preview**: Generates website preview images using Playwright
- **Caching System**: Redis-based caching for optimized performance
- **Asynchronous Processing**: Celery task queue for handling time-intensive operations

## 🛠 Technology Stack

- **Framework**: Flask (Async)
- **Database**: PostgreSQL
- **Cache**: Redis
- **Task Queue**: Celery
- **AI/ML**: 
  - Google Gemini API
  - RAKE (Rapid Automatic Keyword Extraction)
- **Web Scraping**: Playwright
- **Storage**: AWS S3 (for preview images)


## Project Structure
```
.
├── src/
│   ├── utils/
│   │   ├── llm.py.        # Main Question Generator
│   │   ├── scraper.py.    # Webscraping class
│   │   └── utils.py.      # Helper functions
│   ├── app.py.            # Flask app entry point
│   ├── models.py.         # Definition of Postgres models
│   ├── db.py              # database session initializer
│   ├── task.py            # Celery worker file
│   └── crud.py            # Basic DB access functions
└── tests/
```


## 📋 Prerequisites

```bash
# Python version
Python 3.8+

# System Requirements
Redis Server
PostgreSQL
Node.js (for Playwright)
```

## 🔧 Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [project-directory]
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Unix
.\venv\Scripts\activate   # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
playwright install
```

4. Set up environment variables:
```bash
# Create .env file with following variables
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_BUCKET=your_bucket_name
GEMINI_API_KEY=your_gemini_api_key
```

5. Initialize database:
```bash
python -m src.models
```

## 🚀 Running the Application

1. Start Redis server:
```bash
redis-server
```

2. Start Celery worker:
```bash
python -m src.tasks
```

3. Run Flask application:
```bash
flask run
```

## 📡 API Endpoints

### 1. Generate Content
```http
GET /generate-content/?url={website_url}
```
Initiates website analysis and question generation process.

#### Request Parameters
- `url` (required): Website URL to analyze

#### Response
```json
{
    "session_id": "uuid-string",
    "links": ["url1", "url2", ...]
}
```

### 2. Get Preview Image
```http
GET /preview-img/?url={website_url}
```
Generates and returns website preview image.

#### Request Parameters
- `url` (required): Website URL to capture

#### Response
```json
{
    "image": "s3-image-url"
}
```

### 3. Stream Questions
```http
GET /stream/{session_id}
```
SSE endpoint for receiving generated questions in real-time.

#### Request Parameters
- `session_id` (required): Session ID received from generate-content endpoint

#### Stream Events
```json
{
    "question": "Question text",
    "options": ["Option 1", "Option 2", "Option 3"]
}
```

## 🔄 Data Flow

1. Client requests website analysis
2. System scrapes main URL and sublinks
3. Content is processed through:
   - RAKE algorithm for keyword extraction
   - Gemini AI for question generation
4. Questions are streamed to client via SSE
5. Preview image is generated and stored in S3

## ⚠️ Error Handling

The API implements following error responses:

- `400 Bad Request`: Missing or invalid parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side processing errors

## 🔒 Caching Strategy

- **URL Links**: Cached in Redis with URL:links as key
- **Preview Images**: Cached with URL:img as key
- **Cache Duration**: 24 hours default TTL

## 🔍 Monitoring

- Celery task monitoring
- Redis cache hit/miss metrics
- API endpoint response times


## 📄 License

[License Type] - see LICENSE.md for details