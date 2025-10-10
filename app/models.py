
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
from typing import List


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
#add in Marshmallow



#junction table for many-to-many relationship between Ticket and Mechanic
ticket_mechanics = db.Table(
    'ticket_mechanics',
    db.Column('ticket_id', db.ForeignKey('service_tickets.id')),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'))
)

# Create our models
class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)

    #relationship (one-to-many)
    service_tickets: Mapped[List["Ticket"]] = db.relationship(back_populates="customer")

class Ticket(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(17), nullable=False, unique=True)
    service_date: Mapped[date] = mapped_column(db.Date(), nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    # this column in service_tickets table points to the id column in customers table
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))

    #relationship (many-to-one)
    # relationship() lets SQLAlchemy automatically map those database links into python objects
    customer: Mapped["Customer"] = db.relationship(back_populates="service_tickets")
    mechanics: Mapped[List["Mechanic"]] = db.relationship(secondary="ticket_mechanics", back_populates="service_tickets")


class Mechanic(Base):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    salary: Mapped[float] = mapped_column(db.Float(15), nullable=False)

    #relationship (many-to-many)
    service_tickets: Mapped[List["Ticket"]] = db.relationship(secondary="ticket_mechanics", back_populates="mechanics")
