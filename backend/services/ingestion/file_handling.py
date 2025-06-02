import json
import logging
import os
from pathlib import Path

import aiofiles
from fastapi import HTTPException, UploadFile

from core.config import settings

logger = logging.getLogger(__name__)

UPLOAD_DIR = settings.paths.base_dir / settings.paths.upload_dir
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


async def save_file_locally(file: UploadFile, store_path: Path) -> None:
    try:
        store_path.mkdir(parents=True, exist_ok=True)
        file_path = store_path / file.filename

        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)

        await file.seek(0)  #
    except Exception as e:
        logger.error(f"Error saving file locally: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def delete_file_locally(file_path: Path):
    """
    Deletes the file from the local filesystem
    """
    if os.path.exists(file_path):
        os.remove(file_path)
    return True
