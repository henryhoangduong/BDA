import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.chat_routes import chat
from api.database_routes import database_route
from api.dataset_routes import dataset_route
from api.embedding_routes import embedding_route
from api.ingestion_routes import ingestion
from api.parsing_routes import parsing
from core.config import settings
from core.utils.logger import setup_logging

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"


load_dotenv()

setup_logging(level=logging.INFO)

logger = logging.getLogger(__name__)

logger.info("=" * 50)
logger.info("Initializing Application Settings")
logger.info(
    f"TOKENIZERS_PARALLELISM set to: {os.environ['TOKENIZERS_PARALLELISM']}")
logger.info("=" * 50)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Log configuration details on startup"""
    logger.info("=" * 50)
    logger.info("Starting SIMBA Application")
    logger.info("=" * 50)

    # Project Info
    logger.info(f"Project Name: {settings.project.name}")
    logger.info(f"Version: {settings.project.version}")

    # Model Configurations
    logger.info("\nModel Configurations:")
    logger.info(f"LLM Provider: {settings.llm.provider}")
    logger.info(f"LLM Model: {settings.llm.model_name}")
    logger.info(f"Embedding Provider: {settings.embedding.provider}")
    logger.info(f"Embedding Model: {settings.embedding.model_name}")
    logger.info(f"Embedding Device: {settings.embedding.device}")

    # Vector Store & Database
    logger.info("\nStorage Configurations:")
    logger.info(f"Vector Store Provider: {settings.vector_store.provider}")
    logger.info(f"Database Provider: {settings.database.provider}")

    # Paths
    logger.info("\nPaths:")
    logger.info(f"Base Directory: {settings.paths.base_dir}")
    logger.info(f"Upload Directory: {settings.paths.upload_dir}")
    logger.info(f"Vector Store Directory: {settings.paths.vector_store_dir}")

    logger.info("=" * 50)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(parsing, tags=["Parse"], prefix="/api")
app.include_router(ingestion, tags=["Ingestion"], prefix="/api")
app.include_router(embedding_route, tags=["Embedding"], prefix="/api")
app.include_router(chat, tags=["Chat"], prefix="/api")
# app.include_router(database_route, tags=["Database"], prefix="/api")
# app.include_router(dataset_route, tags=["Dataset"], prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)
