from pydantic import BaseModel, Field
from utils.enums import EventStatus
from schemas.examples import ExampleEvent
from datetime import datetime, time as t, date




class BaseEventSchema(BaseModel):
    title: str = Field(examples=[ExampleEvent.title])
    description: str = Field(examples=[ExampleEvent.description])
    category: str = Field(examples=[ExampleEvent.category])
    
    start_date: date = Field(examples=[ExampleEvent.start_date])
    end_date: date = Field(examples=[ExampleEvent.end_date])
    time: t = Field(examples=[ExampleEvent.time])
    
    ticket_price: int = Field(examples=[ExampleEvent.ticket_price])
    max_ticket: int = Field(examples=[ExampleEvent.max_ticket])
    location: str = Field(examples=[ExampleEvent.location])


class EventRequestSchema(BaseEventSchema):
    pass


class EventResponseSchema(BaseEventSchema):
    organizer_id: int = Field(examples=[ExampleEvent.organizer_id])
    id: int = Field(examples=[ExampleEvent.id])
    
    created_at: datetime = Field(examples=[ExampleEvent.created_at])
    status: EventStatus = Field(examples=[ExampleEvent.status])
    
    
    
class EventEditRequestSchema(BaseEventSchema):
    status: EventStatus = Field(examples=[ExampleEvent.status])