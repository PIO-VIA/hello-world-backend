from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.logging_config import logger

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
