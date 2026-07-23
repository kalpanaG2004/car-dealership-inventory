from functools import lru_cache

from pymongo import MongoClient
from pymongo.database import Database

from app.config import get_settings


@lru_cache
def get_mongo_client() -> MongoClient:
    return MongoClient(get_settings().mongodb_url)


def get_database() -> Database:
    """Provide the configured MongoDB database to API endpoints."""
    settings = get_settings()
    return get_mongo_client()[settings.mongodb_database]
