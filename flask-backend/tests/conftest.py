import os
import pytest

# Load environment variables for testing
pytest.register_assert_rewrite('tests.test_routes', 'tests.test_scraper')

def pytest_configure(config):
    """
    Allows plugins and internal configurations prior to test run.
    """
    # Set up test-specific environment variables
    os.environ.setdefault('TESTING', 'True')
    os.environ.setdefault('DATABASE_URL', 'postgresql+asyncpg://postgres:nedu@localhost:5432/chatsimple_test')


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """
    Mock critical environment variables for testing
    """
    monkeypatch.setenv('AWS_ACCESS', 'test-access-key')
    monkeypatch.setenv('AWS_SECRET', 'test-secret-key')
    monkeypatch.setenv('GEMINI_KEY', 'test-gemini-key')
    monkeypatch.setenv('ARLIAI_API_KEY', 'test-arliai-key')