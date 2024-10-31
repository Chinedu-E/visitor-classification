export interface Question {
    question: string;
    options: string[];
  }
  
  export interface GenerateContentResponse {
    session_id: string;
    links: string[];
  }
  
  export interface PreviewImageResponse {
    image: string;
  }
  
  export interface SSEMessage {
    link?: string;
    questions?: Question[];
    status?: 'complete';
    error?: string;
  }
  
  export interface UserAnswer {
    questionIndex: number;
    answer: string;
  }
  