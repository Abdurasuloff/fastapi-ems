"""Define Schemas used by the Events routets"""


from datetime import date, datetime, time as t
from pydantic import BaseModel, ConfigDict, Field
from schemas.examples import ExampleEvent
from utils.enums import EventStatus

class EventBase(BaseModel):
    """Base for the Event Schema."""

    title: str = Field(examples=[ExampleEvent.title])
    description: str = Field(examples=[ExampleEvent.description])
    category: str = Field(examples=[ExampleEvent.category])
    
    start_date: date = Field(examples=[ExampleEvent.start_date])
    end_date: date = Field(examples=[ExampleEvent.end_data])
    time: t = Field(examples=[ExampleEvent.time])
    
    ticket_price: int = Field(examples=[ExampleEvent.ticket_price])
    max_ticket: int = Field(examples=[ExampleEvent.max_ticket])
    
    location: str = Field(examples=[ExampleEvent.location])
    
    



class EventRequestSchema(EventBase):
    pass


class EventResponseSchema(EventBase):
    organizer_id: int = Field(examples=[45])
    id: int = Field(examples=[ExampleEvent.id])
    created_at: datetime =  Field(examples=[ExampleEvent.created_at])
    status: EventStatus = Field(examples=[ExampleEvent.status])