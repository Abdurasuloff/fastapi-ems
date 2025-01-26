"""Define the User manager."""

from typing import Any, Optional, Type
from email_validator import EmailNotValidError, validate_email
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import delete, update
from sqlalchemy.exc import IntegrityError
from database.helpers import EventDB, UserDB
from managers.auth import AuthManager
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.event_schemas import EventRequestSchema, EventResponseSchema
from models import Event


class EventManager:
    """Class to Manage the User."""

    @staticmethod
    async def create(event_data: EventRequestSchema, organizer_id: int, session: AsyncSession) -> EventResponseSchema:
        """Create a new event and return it with its ID."""
        try:
            event_data_dict = event_data.model_dump()
            event_data_dict["organizer_id"] = organizer_id

            new_event = Event(**event_data_dict)
            session.add(new_event)
            await session.flush()
            await session.refresh(new_event)

            return new_event
                
        except Exception as err:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Something went wrong. Why: {err}") from err

      