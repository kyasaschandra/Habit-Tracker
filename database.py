"""
Database models for the Personal Dashboard App.
This module defines all database tables using SQLAlchemy ORM.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Base class for all database models
Base = declarative_base()


class Habit(Base):
    """
    Stores habit information.
    Each habit has a unique ID and name.
    """
    __tablename__ = 'habits'

    # Primary key - unique identifier for each habit
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Name of the habit (e.g., "Exercise", "Read", "Meditate")
    name = Column(String(200), nullable=False)

    # Date when the habit was created
    created_date = Column(Date, default=datetime.now().date)

    # Relationship to habit entries (one habit can have many entries)
    entries = relationship("HabitEntry", back_populates="habit", cascade="all, delete-orphan")


class HabitEntry(Base):
    """
    Stores individual habit completions for specific dates.
    Each entry represents a habit being checked on a particular day.
    """
    __tablename__ = 'habit_entries'

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign key linking to the habit
    habit_id = Column(Integer, ForeignKey('habits.id'), nullable=False)

    # Date when the habit was completed
    date = Column(Date, nullable=False)

    # Whether the habit was completed (True) or not (False)
    completed = Column(Boolean, default=True)

    # Relationship back to the habit
    habit = relationship("Habit", back_populates="entries")


class Expense(Base):
    """
    Stores expense/spending records.
    Each record contains date, amount, card used, category, and description.
    """
    __tablename__ = 'expenses'

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Date of the expense
    date = Column(Date, nullable=False)

    # Amount spent (stored as float for decimal values)
    amount = Column(Float, nullable=False)

    # Name of the card used for payment
    card_used = Column(String(100), nullable=False)

    # Category of spending (e.g., "Food", "Transport", "Entertainment")
    category = Column(String(100), nullable=False)

    # Description of the expense
    description = Column(String(500))


class Card(Base):
    """
    Stores credit/debit card information and debt.
    Used for tracking total debt per card.
    """
    __tablename__ = 'cards'

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Name of the card (e.g., "Visa Gold", "HDFC Credit")
    card_name = Column(String(100), nullable=False, unique=True)

    # Total debt on this card
    debt = Column(Float, default=0.0)


# Database file path (SQLite database)
DATABASE_URL = "sqlite:///dashboard.db"

# Create database engine
engine = create_engine(DATABASE_URL, echo=False)

# Create session maker for database operations
SessionLocal = sessionmaker(bind=engine)


def init_database():
    """
    Initialize the database by creating all tables.
    This function should be called once when the app starts.
    """
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")


def get_db_session():
    """
    Create and return a new database session.

    Returns:
        Session: SQLAlchemy database session
    """
    return SessionLocal()
