from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table,MetaData, ForeignKeyConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from faker import Faker
import random

Base = declarative_base()

metadata = MetaData()

flights = Table('flights', metadata,
    Column('id', Integer, primary_key=True),
    Column('plane_name', String(255)),
    Column('takeoff_time', Integer),
    Column('price', Integer),
    Column('destination', String(255)),
    Column('pilot_id',Integer),
    ForeignKeyConstraint(['pilot_id'], ['pilots.id']) # Assuming you have a pilot_id column
)

class Flight(Base):
    __table__ = flights
    pilot = relationship("Pilot", back_populates="flights")

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    flight_id = Column(Integer)
    ForeignKeyConstraint(['flight_id'], ['flights.id'])

# class Flight(Base):
#     __tablename__ = 'flights'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     plane_name = Column(String(255))
#     takeoff_time = Column(Integer)
#     price = Column(Integer)
#     destination = Column(String(255))
#     pilot_id = Column(Integer, ForeignKey('pilots.id'))
    

pilots = Table('pilots', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('current_flight_id', Integer),
      # Assuming you have a flights table
)

class Pilot(Base):
    __table__ = pilots
    flights = relationship("Flight", back_populates="pilot")

engine = create_engine('sqlite:///flights.db')
Base.metadata.create_all(engine)

# Creating Faker instance
fake = Faker()

# Function to generate random flights
# def generate_random_flights(session, count=10):
#     for _ in range(count):
#         id = None
#         flight = Flight(
#             plane_name=fake.name(),
#             takeoff_time=fake.date_time_this_decade().hour * 100,
#             price=random.randint(100, 1000),
#             destination=fake.city(),
#             pilot_id=random.randint(1, 10)
#         )
#         session.add(flight)

# Create session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Generate 10 random flights
# generate_random_flights(session, count=10)

# Commit changes
session.commit()

