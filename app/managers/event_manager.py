"""Define the Event manager."""
from collections.abc import Sequence
from fastapi import HTTPException, status
from sqlalchemy import delete, update
from models import Event
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.events_schemas import EventRequestSchema, EventResponseSchema, EventEditRequestSchema
from database.helpers import EventDB



class EventManager:
    """Class to Manage the Event."""

    @staticmethod
    async def create_event(event_data: EventRequestSchema, organizer_id: int, session: AsyncSession) -> EventResponseSchema:

        """Create a event."""
        try:
            new_event_data = event_data.model_dump()
            new_event_data["organizer_id"] = organizer_id
            
            event = Event(**new_event_data)
            session.add(event)
            await session.flush()
            await session.refresh(event)
            
            return event

        except Exception as err:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Something went wrong. Why: {err}") from err

    
    @staticmethod
    async def get_event(event_id: int, session: AsyncSession) -> EventResponseSchema:
        """Get a event by its id"""
        
        event = await EventDB.get(session, event_id)
        if event is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Event is not found with id: {event_id}")
        return event
        
        
        
    @staticmethod
    async def get_all_events(session: AsyncSession) -> Sequence[Event]:
        """Get all events"""
        
        try:
            events = await EventDB.all(session)
            return events
        
        except Exception as err:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Something went wrong wih getting al events. Why: {err}") from err
        
        
        
    @staticmethod
    async def update_event(event_id: int, organizer_id: int,  event_data: EventEditRequestSchema, session: AsyncSession) -> None:
        """Updaete the event"""
        
        check_event = await EventDB.get(session, event_id)
        if not check_event:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Event is not found with this id: {event_id}")
        
        if check_event.organizer_id != organizer_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Event is not author of this event")
        
        
        await session.execute(
            update(Event).where(Event.id == event_id).values(
                title = event_data.title,
                description = event_data.description,
                category = event_data.category,
                start_date = event_data.start_date,
                end_date = event_data.end_date,
                time = event_data.time,
                ticket_price = event_data.ticket_price,
                max_ticket = event_data.max_ticket,
                location = event_data.location,
                status = event_data.status
            )
        )
        
        await session.refresh(check_event)
        return check_event
    
    
    
    @staticmethod
    async def delete_event(event_id: int, organizer_id: int,  session: AsyncSession) -> None:
        """Delete the Event with specified ID."""
        check_event = await EventDB.get(session, event_id)
        if not check_event :
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Event is not found with this id: {event_id}")
        
        if check_event.organizer_id != organizer_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Event is not author of this event")

        await session.execute(delete(Event).where(Event.id == event_id))