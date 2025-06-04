from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from fastapi import UploadFile


class StorageProvider(ABC):

    @abstractmethod
    async def save_file(self, file_path: Path, file: UploadFile) -> Path:
        pass

    @abstractmethod
    async def get_file(self, file_path: Path) -> Optional[bytes]:
        pass

    @abstractmethod
    async def delete_file(self, file_path: Path) -> bool:
        pass

    @abstractmethod
    async def file_exists(self, file_path: Path) -> bool:
        pass
