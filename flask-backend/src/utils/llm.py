import os
import json
from typing import Tuple, List, Optional
from rake_nltk import Rake
import google.generativeai as genai
from dotenv import load_dotenv
from openai import OpenAI
import requests
from typing_extensions import TypedDict



load_dotenv()  # take environment variables from .env.

genai.configure(api_key=os.getenv("GEMINI_KEY", ""))
ARLIAI_API_KEY = os.getenv("ARLIAI_API_KEY")

class Analysis(TypedDict):
    topics: list[str]
    industry: list[str]
    target_audience: str
    
class Question(TypedDict):
    question: str
    answer: str
    options: list[str]
    
json_schema = {
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "question": {
        "type": "string"
      },
      "options": {
        "type": "array",
        "items": {
          "type": "string"
        }
      }
    },
    "required": [
      "question",
      "answer"
    ]
  }
}

class UrlInfo(TypedDict):
    url: str
    main_page_text: str
    links: list[str]
    link_texts: dict[str, str]


class QuestionGenerator:
    
    def __init__(self, url_info: UrlInfo):
        self.rake = Rake(include_repeated_phrases=False)
        self.model = genai.GenerativeModel("gemini-1.5-pro")
        self.url_info = url_info
        
    def extract_all_keywords(self):
        main_page_keywords = self._extract_keywords(self.url_info['main_page_text'], num_keywords=10)
        sublink_keywords = {
            link: self._extract_keywords(text, num_keywords=5) 
            for link, text in self.url_info['link_texts'].items()
        }
        keywords = {
            'main_page_keywords': main_page_keywords,
            'sublink_keywords': sublink_keywords
        }
        return keywords
        
    
    def _extract_keywords(
        self, 
        text: str, 
        num_keywords: int = 30
    ) -> List[Tuple[str, float]]:
        
        self.rake.extract_keywords_from_text(text)
        keywords = self.rake.get_ranked_phrases_with_scores()
        return [(keyword, score) for score, keyword in keywords[: num_keywords]]
    
    def _get_text_analysis(self, keywords: dict) -> Analysis:
        prompt = f"""
            Analyze this website main content and its sublinks with their keywords and identify the main topics, industry, and target audience
            main content: {self.url_info['main_page_text']}
            keywords: {keywords}
        """
        result = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=Analysis
            ),
        )
        return json.loads(result.text)
        
    def generate_questions(self):
        keywords = self.extract_all_keywords()
        analysis = self._get_text_analysis(keywords)
        print(analysis)
        prompt = f"""
            Based on this website analysis: {analysis}
            and its sublink keywords: {keywords['sublink_keywords']}
            Generate FOUR (4) multiple choice questions that are very specific to this website that would help categorize visitors:
        """
        url = "https://api.arliai.com/v1/chat/completions"

        payload = json.dumps({
            "model": "Meta-Llama-3.1-8B-Instruct",
            "messages": [{
            "role": "system",
            "content": "You are a helpful assistant that generates survey questions."
        }, {
            "role": "user",
            "content": prompt
        }],
            "repetition_penalty": 1.1,
            "temperature": 1,
            "top_p": 0.9,
            "top_k": 40,
            "guided_json": json_schema,
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {ARLIAI_API_KEY}"
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        res =  response.json()
        questions = res["choices"][0]['message']['content']
        if (isinstance(questions, str)):
            questions = json.loads(questions)
        return questions
    
        """result = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=list[Question],
            ),
        )
        print(result)
        return json.loads(result.text)"""
        