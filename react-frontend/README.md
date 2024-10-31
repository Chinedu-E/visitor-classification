# Website Visitor Classification Tool

## Overview
A dynamic web application built with Next.js and Redux that analyzes website content and generates personalized questions to classify visitors based on their interests and industry. This tool takes a URL input, scrapes the website content, and provides an interactive questionnaire for visitor categorization.

## Features
- **URL Input & Validation**: Easy-to-use interface for submitting website URLs
- **Website Preview**: Visual preview of the target website with loading skeleton
- **Real-time Question Generation**: 
  - Server-Sent Events (SSE) integration for streaming questions
  - Dynamic multiple-choice options
  - Progress indicator during question generation
- **State Management**: 
  - Centralized Redux store for managing user responses
  - Persistent state across question sets
- **Loading States**:
  - Skeleton loaders for link previews
  - Loading progress bar for question generation
  - Smooth loading transitions

## Tech Stack
- Next.js
- Redux for state management
- Server-Sent Events (SSE) for real-time updates
- TailwindCSS for styling

## Getting Started

### Prerequisites
- Node.js (Latest LTS version recommended)
- npm or yarn

### Installation

1. Clone the repository
```bash
git clone [your-repository-url]
cd [project-directory]
```

2. Install dependencies
```bash
npm install
# or
yarn install
```

3. Environment Setup
Create a `.env.local` file in the root directory and add:
```
NEXT_PUBLIC_BACKEND_URL=your_backend_url_here
```

4. Start the development server
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

## Usage

1. Enter a website URL in the input field
2. Wait for the preview to load and website content to be analyzed
3. Answer the dynamically generated questions
4. View the classification results based on your responses

## Project Structure
```
.
└── src/
    ├── components/       # Reusable UI components
    ├── app/              # Next.js pages (App router)
    ├── store/            # Redux (store, slices, apiQuery and data types)
    ├── services/         # Class for SSE implementation
    └── lib/              # Utility functions and helpers
```


### Running Tests
```bash
npm test
# or
yarn test
```

### Building for Production
```bash
npm run build
# or
yarn build
```


## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details