# pylint: disable=invalid-name
"""Define Enums for this project."""

from enum import Enum


class RoleType(Enum):
    """Contains the different Role types Users can have."""

    user = "user"
    admin = "admin"
    organizer = "organizer"


class EventStatus(Enum):
    """ To represent the status of the Events"""
    
    not_started = "not_started"
    countinuing = "countinuing"
    finished = "finished"
    canceled = "canceled"
    
    
    
class TicketStatus(Enum):
    
    available = "available"
    not_available = "not_available"
    

class PaymentStatus(Enum):
   
    pending = "pending"
    approved = "approved"
    declided = "declined"
    out_of_balance = "out_of_balance"
    
   
class PaymentMethod(Enum):
    cash = "cash"
    card = "card"