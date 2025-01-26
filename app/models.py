"""Define the Users model."""

from datetime import date, datetime, time as t
from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, Integer, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import Base
from utils.enums import RoleType, EventStatus, TicketStatus, PaymentMethod, PaymentStatus


class User(Base):
    """Define the Users model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(50))
    role: Mapped[RoleType] = mapped_column(
        Enum(RoleType),
        nullable=False,
        server_default=RoleType.user.value,
        index=True,
    )
    banned: Mapped[bool] = mapped_column(Boolean, default=False)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    events: Mapped[list["Event"]] = relationship()
    tickets: Mapped[list["Ticket"]] = relationship()
    payments: Mapped[list["Payment"]] = relationship()

    def __repr__(self) -> str:
        """Define the model representation."""
        return f'User({self.id}, "{self.first_name} {self.last_name}")'
    
    
    
class Event(Base):
    """Define the Events model."""
    __tablename__ = "events"

    organizer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    organizer: Mapped[User] = relationship("User", back_populates="events")

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50))

    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    time: Mapped[t] = mapped_column(Time)

    ticket_price: Mapped[int] = mapped_column(Integer)
    max_ticket: Mapped[int] = mapped_column(Integer)

    location: Mapped[str] = mapped_column(String(120))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    status: Mapped[EventStatus] = mapped_column(
        Enum(EventStatus),
        nullable=False,
        server_default=EventStatus.not_started.value,
        index=True,
    )

    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="event")

    def __repr__(self) -> str:
        return f'Event({self.id}, "{self.title}")'



class Ticket(Base):
    """Define the model Ticket"""
    __tablename__ = "tickets"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship("User", back_populates="tickets")

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    event: Mapped[Event] = relationship("Event", back_populates="tickets")

    id: Mapped[int] = mapped_column(primary_key=True)

    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus),
        nullable=False,
        server_default=TicketStatus.not_available.value,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    payments: Mapped[list["Payment"]] = relationship()

    def __repr__(self) -> str:
        return f'Ticket({self.id})'
    
    
    
class Payment(Base):
    """Define the Payment Model"""
    
    __tablename__ = 'payments'
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship("User", back_populates="payments")
    
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"))
    ticket: Mapped[Ticket] = relationship("Ticket", back_populates="payments")
    
    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column(Integer())
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    
    payment_method: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod), 
        nullable=False, 
        server_default=PaymentMethod.cash.value)
    card_number: Mapped[str] = mapped_column(String(length=16), nullable=True)
    exp_date: Mapped[str] = mapped_column(String(length=5), nullable=True)
    
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus), 
        nullable=False, 
        server_default=PaymentStatus.pending.value)
    
    def __repr__(self) -> str:
        """Define the model representation."""
        return f'Payment({self.id})'
    