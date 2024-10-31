# Website Visitor Classification System

## Project Overview
A full-stack web application that analyzes websites and generates dynamic questions to classify visitors based on their interests and industry. The system takes a URL input, processes the website content, and creates personalized questionnaires for visitor categorization.

## Project Structure

```
.
├── react-frontend/     # Next.js frontend application
├── flask-backend/      # Flask backend service
└── README.md          # This file
```

### Frontend (`/react-frontend`)
The frontend is built with Next.js and Redux, providing an interactive user interface for:
- URL submission and validation
- Website content preview
- Real-time question generation and display
- User response management

➡️ [View Frontend Documentation](./react-frontend/README.md)

### Backend (`/flask-backend`)
The backend service is built with Flask, handling:
- Website content scraping
- Natural language processing
- Question generation
- Server-sent events for real-time updates

➡️ [View Backend Documentation](./flask-backend/README.md)

## Quick Start

1. Start the Backend:
```bash
cd flask-backend
# Follow setup instructions in flask-backend/README.md
```

2. Start the Frontend:
```bash
cd react-frontend
# Follow setup instructions in react-frontend/README.md
```

## Note for Reviewers
- Each directory contains its own detailed README with specific setup instructions and documentation
- The frontend and backend are designed to work together but can be started independently
- Please refer to individual README files for detailed setup instructions and available features