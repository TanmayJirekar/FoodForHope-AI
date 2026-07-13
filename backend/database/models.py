from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from backend.database.database import Base

class RoleEnum(str, enum.Enum):
    donor = "donor"
    ngo = "ngo"
    admin = "admin"

class DonationStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    volunteer_assigned = "volunteer_assigned"
    in_transit = "in_transit"
    collected = "collected"
    delivered = "delivered"
    completed = "completed"
    rejected = "rejected"

class FoodSafetyStatus(str, enum.Enum):
    safe = "SAFE"
    moderately_safe = "MODERATELY_SAFE"
    unsafe = "UNSAFE"
    spoiled = "SPOILED"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Donor(Base):
    __tablename__ = "donors"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(500))
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(20))
    latitude = Column(Float)
    longitude = Column(Float)
    
    user = relationship("User")
    donations = relationship("FoodDonation", back_populates="donor")

class NGO(Base):
    __tablename__ = "ngos"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    ngo_name = Column(String(255), nullable=False)
    registration_number = Column(String(100), unique=True)
    owner_name = Column(String(255))
    phone = Column(String(20), nullable=False)
    address = Column(String(500))
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(20))
    latitude = Column(Float)
    longitude = Column(Float)
    description = Column(Text)
    working_areas = Column(String(255))
    is_verified = Column(Boolean, default=False)
    
    user = relationship("User")
    accepted_donations = relationship("FoodDonation", back_populates="ngo")
    volunteers = relationship("Volunteer", back_populates="ngo")

class FoodDonation(Base):
    __tablename__ = "food_donations"
    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("donors.id"))
    ngo_id = Column(Integer, ForeignKey("ngos.id"), nullable=True)
    
    food_name = Column(String(255))
    food_type = Column(String(100))
    quantity = Column(Float) # in kg or items
    persons_served = Column(Integer)
    preparation_time = Column(DateTime)
    storage_method = Column(String(100))
    storage_temperature = Column(Float)
    packaging_type = Column(String(100))
    expiry_time = Column(DateTime)
    pickup_address = Column(String(500))
    pickup_time = Column(DateTime)
    additional_notes = Column(Text)
    
    image_url = Column(String(500))
    
    # AI Results
    safety_score = Column(Float)
    safety_status = Column(Enum(FoodSafetyStatus))
    safety_reason = Column(Text)
    safe_time_remaining = Column(Float) # hours
    
    status = Column(Enum(DonationStatus), default=DonationStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    donor = relationship("Donor", back_populates="donations")
    ngo = relationship("NGO", back_populates="accepted_donations")
    pickup = relationship("PickupRequest", back_populates="donation", uselist=False)

class Volunteer(Base):
    __tablename__ = "volunteers"
    id = Column(Integer, primary_key=True, index=True)
    ngo_id = Column(Integer, ForeignKey("ngos.id"))
    name = Column(String(255))
    phone = Column(String(20))
    vehicle_type = Column(String(100))
    availability = Column(String(255))
    
    ngo = relationship("NGO", back_populates="volunteers")
    pickups = relationship("PickupRequest", back_populates="volunteer")

class PickupRequest(Base):
    __tablename__ = "pickup_requests"
    id = Column(Integer, primary_key=True, index=True)
    donation_id = Column(Integer, ForeignKey("food_donations.id"), unique=True)
    volunteer_id = Column(Integer, ForeignKey("volunteers.id"), nullable=True)
    status = Column(Enum(DonationStatus), default=DonationStatus.pending)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    donation = relationship("FoodDonation", back_populates="pickup")
    volunteer = relationship("Volunteer", back_populates="pickups")
