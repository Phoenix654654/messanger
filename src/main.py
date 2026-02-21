from fastapi import FastAPI, HTTPException
import uvicorn
import re
import uuid
from fastapi.routing import APIRouter
from sqlalchemy import Column, Boolean, String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel, EmailStr, validator

from config.fastapi.base import settings

engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
