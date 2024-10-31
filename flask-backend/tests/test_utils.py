import os
import pytest
import boto3
from unittest.mock import patch, MagicMock
from botocore.exceptions import NoCredentialsError
from src.utils.utils import upload_to_s3, capture_screenshot

@pytest.mark.asyncio
async def test_upload_to_s3():
    """
    Test S3 upload utility function
    """
    # Create a temporary file for testing
    test_file_path = "/tmp/test_upload.png"
    with open(test_file_path, 'wb') as f:
        f.write(b"test content")
    
    bucket_name = "test-bucket"
    object_name = "test-object"
    
    with patch('boto3.client') as mock_boto_client, \
         patch('os.remove') as mock_remove:
        # Mock S3 client
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        
        # Set up environment variables
        os.environ['AWS_ACCESS'] = 'test-access-key'
        os.environ['AWS_SECRET'] = 'test-secret-key'
        
        # Call the function
        result = upload_to_s3(test_file_path, bucket_name, object_name)
        
        # Assertions
        mock_s3_client.upload_file.assert_called_once()
        mock_remove.assert_called_once_with(test_file_path)
        assert result == f"https://{bucket_name}.s3.amazonaws.com/{object_name}"

@pytest.mark.asyncio
async def test_capture_screenshot():
    """
    Test screenshot capture utility function
    Note: Requires Playwright to be installed
    """
    from playwright.async_api import async_playwright
    
    test_url = "https://www.apple.com"
    
    async with async_playwright() as p:
        screenshot_path = await capture_screenshot(test_url)
        
        # Verify screenshot was created
        assert os.path.exists(screenshot_path)
        assert screenshot_path.endswith('.png')
        
        # Clean up
        os.remove(screenshot_path)


def test_upload_to_s3_no_credentials():
    """
    Test S3 upload with missing credentials
    """
    test_file_path = "/tmp/test_upload.png"
    with open(test_file_path, 'wb') as f:
        f.write(b"test content")
    
    # Unset credentials
    with patch.dict(os.environ, {}, clear=True), \
         patch('boto3.client') as mock_boto_client:
        
        mock_boto_client.side_effect = NoCredentialsError
        
        try:
            result = upload_to_s3(test_file_path, "test-bucket", "test-object")
        except NoCredentialsError:
            result = None

        assert result is None