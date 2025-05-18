import asyncio
import os
import sys
import warnings
from glob import glob

import aiofiles
from dotenv import load_dotenv
from langsmith import traceable
from pyzerox import zerox

# Ensure UTF-8 encoding globally
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
os.environ["PYTHONIOENCODING"] = "utf-8"

# Load environment variables
load_dotenv()


model = "gpt-4o-mini"
pdft_path_directory = "Documents/Vie/pdf"
output_dir = "Markdown"
custom_system_prompt = """Convert the following PDF page to markdown.
Return only the markdown with no explanation text.
Do not exclude any content from the page.
Be careful with big tables. If a table spans multiple pages, reconstruct it as a single table.
"""

os.environ["OPENAI_API_KEY"] = os.getenv("AS_OPENAI_API_KEY")


@traceable
async def process_file(file_path):
    select_pages = None

    # Ensure the ouput directory exists
    os.makedirs(output_dir, exist_ok=True)

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="Custom system prompt was provided*")
        try:
            raw_result = await zerox(file_path=file_path, model=model)
        except Exception as e:
            print(f"Error processing {file_path}: {e}", file=sys.stderr)
