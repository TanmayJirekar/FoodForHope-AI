from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from backend.database.models import RoleEnum, DonationStatus, FoodSafetyStatus

# --- Users & Auth ---
class UserBase(BaseModel):
    email: EmailStr
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: RoleEnum
    user_id: int

# --- Donors ---
class DonorCreate(UserCreate):
    full_name: str
    phone: str
    address: str
    city: str
    state: str
    pincode: str
    latitude: float
    longitude: float

# --- NGOs ---
class NGOCreate(UserCreate):
    ngo_name: str
    registration_number: str
    owner_name: str
    phone: str
    address: str
    city: str
    state: str
    pincode: str
    latitude: float
    longitude: float
    description: str
    working_areas: str

class NGOResponse(BaseModel):
    id: int
    ngo_name: str
    address: str
    city: str
    phone: str
    latitude: float
    longitude: float
    
    class Config:
        from_attributes = True

# --- Donations ---
class FoodDonationCreate(BaseModel):
    food_name: str
    food_type: str
    quantity: float
    persons_served: int
    preparation_time: datetime
    storage_method: str
    storage_temperature: float
    packaging_type: str
    expiry_time: datetime
    pickup_address: str
    pickup_time: datetime
    additional_notes: Optional[str] = None

class FoodDonationResponse(FoodDonationCreate):
    id: int
    donor_id: int
    ngo_id: Optional[int]
    image_url: Optional[str]
    safety_score: Optional[float]
    safety_status: Optional[FoodSafetyStatus]
    safety_reason: Optional[str]
    safe_time_remaining: Optional[float]
    status: DonationStatus
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Volunteers ---
class VolunteerCreate(BaseModel):
    name: str
    phone: str
    vehicle_type: str
    availability: str

class VolunteerResponse(VolunteerCreate):
    id: int
    ngo_id: int
    
    class Config:
        from_attributes = True

# --- AI Responses ---
class AISafetyResponse(BaseModel):
    safety_score: float
    safety_status: str
    safety_reason: str
    safe_time_remaining: float
