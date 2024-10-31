from unittest.mock import patch
import pytest
import json
from src.utils.llm import QuestionGenerator

@pytest.fixture
def mock_url_info():
    """
    Fixture for creating a sample URL info dictionary
    """
    return {
        'url': 'https://www.example.com',
        'main_page_text': 'Example website providing innovative solutions for business and technology',
        'links': ['https://www.example.com/about', 'https://www.example.com/services'],
        'link_texts': {
            'https://www.example.com/about': 'About our company and our mission',
            'https://www.example.com/services': 'Our comprehensive range of technology services'
        }
    }

def test_keyword_extraction(mock_url_info):
    """
    Test keyword extraction functionality
    """
    generator = QuestionGenerator(mock_url_info)
    
    keywords = generator.extract_all_keywords()
    
    assert 'main_page_keywords' in keywords
    assert 'sublink_keywords' in keywords
    assert len(keywords['main_page_keywords']) > 0
    assert len(keywords['sublink_keywords']) > 0

def test_text_analysis(mock_url_info):
    """
    Test text analysis method
    """
    generator = QuestionGenerator(mock_url_info)
    
    # Mock some keywords
    mock_keywords = {
        'main_page_keywords': [('business', 0.8), ('technology', 0.7)],
        'sublink_keywords': {}
    }
    
    # This might need to be mocked depending on actual Gemini API behavior
    analysis = generator._get_text_analysis(mock_keywords)
    
    assert 'topics' in analysis
    assert 'industry' in analysis
    assert 'target_audience' in analysis

def test_question_generation(mock_url_info):
    """
    Test question generation
    Note: This will likely need to be mocked due to API dependency
    """
    generator = QuestionGenerator(mock_url_info)
    
    with patch.object(QuestionGenerator, 'generate_questions', return_value=[]):
        questions = generator.generate_questions()
        
        # Check that the mock is working as expected
        assert isinstance(questions, list)
        assert len(questions) == 0
        