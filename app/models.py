from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Flight(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    plane_name = Column(String(255))
    takeoff_time = Column(Integer)
    price = Column(Integer)
    destination = Column(String(255))
    pilot_id = Column(Integer, ForeignKey('pilots.id'))

    pilot = relationship("Pilot", back_populates="flights")
    customers = relationship('Customer', back_populates='flight')

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    flight_id = Column(Integer, ForeignKey('flights.id'))

    flight = relationship('Flight', back_populates='customers')

class Pilot(Base):
    __tablename__ = 'pilots'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    current_flight_id = Column(Integer)

    flights = relationship("Flight", back_populates="pilot")
