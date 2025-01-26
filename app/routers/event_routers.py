"""Routes for Event listing and control."""

from collections.abc import Sequence
from typing import Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_database
from managers.auth import can_edit_user, is_admin, oauth2_schema, is_organizer
from managers.user import UserManager
from managers.event_manager import EventManager
from utils.enums import RoleType
from models import User, Event
from schemas.events_schemas import EventRequestSchema, EventResponseSchema, EventEditRequestSchema

router = APIRouter(tags=["Events"], prefix="/events")


@router.post("/", dependencies=[Depends(oauth2_schema), Depends(is_organizer)], response_model=EventResponseSchema, status_code=201)
async def create_event(request: Request, event_data: EventRequestSchema, db: AsyncSession = Depends(get_database)) -> Event:
    """Create an event

    This route is only allowed for Admins and Organizers.
    """
    event = await EventManager.create_event(event_data, request.state.user.id, db)
    return event



@router.get("/", dependencies=[Depends(oauth2_schema), Depends(is_organizer)], response_model=Union[EventResponseSchema, list[EventResponseSchema]])
async def get_events(event_id: Optional[int] = None, db: AsyncSession = Depends(get_database)) -> Union[Sequence[Event], Event]:
    """Get all events or a specific one by their ID.
    
    This route is only allowed for Admins or Organizers.
    """
    if event_id:
        return await EventManager.get_event(event_id, db)
    return await EventManager.get_all_events(db)


@router.put("/{event_id}", dependencies=[Depends(oauth2_schema), Depends(is_organizer)], status_code=200, response_model=EventResponseSchema)
async def update_event(request: Request, event_id: int, event_data: EventEditRequestSchema, db: AsyncSession = Depends(get_database)) -> Event:
    
    return await EventManager.update_event(
        event_id=event_id,
        event_data=event_data,
        organizer_id=request.state.user.id,
        session=db
    )
    
    
@router.delete("/{event_id}", dependencies=[Depends(oauth2_schema), Depends(is_organizer)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(request: Request, event_id: int, db: AsyncSession = Depends(get_database)) -> None:
    """Delete the specified Event by user_id"""
    await EventManager.delete_event(event_id, request.state.user.id, db)
