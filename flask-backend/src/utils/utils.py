import os
from playwright.async_api import async_playwright
from tempfile import NamedTemporaryFile
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

load_dotenv()


def upload_to_s3(file_path: str, bucket_name: str, object_name: str) -> str:
    """Uploads the file to S3 and returns the public URL."""
    try:
        s3_client = boto3.client('s3', aws_access_key_id=os.getenv("AWS_ACCESS"), aws_secret_access_key=os.getenv('AWS_SECRET'))
        s3_client.upload_file(
            file_path, bucket_name, object_name,
        )
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
    except NoCredentialsError:
        print("Credentials not available")
        return None
    finally:
        os.remove(file_path)  # Clean up the local file
    return s3_url


async def capture_screenshot(url: str) -> str:
    """Captures screenshot of the given URL and saves it temporarily."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        
        # Using NamedTemporaryFile to save screenshot temporarily
        with NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            await page.screenshot(path=temp_file.name, full_page=True)
            temp_file_path = temp_file.name  # Path of the screenshot
        await browser.close()
        
    return temp_file_path