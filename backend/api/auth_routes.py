from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Any

from backend.database import database, models
from backend.schemas import schemas
from backend.services import auth

router = APIRouter()

@router.post("/register/donor", response_model=schemas.Token)
def register_donor(donor_in: schemas.DonorCreate, db: Session = Depends(database.get_db)):
    # Check if user exists
    db_user = db.query(models.User).filter(models.User.email == donor_in.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create User
    hashed_password = auth.get_password_hash(donor_in.password)
    user = models.User(email=donor_in.email, password_hash=hashed_password, role=models.RoleEnum.donor)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create Donor
    donor = models.Donor(
        user_id=user.id,
        full_name=donor_in.full_name,
        phone=donor_in.phone,
        address=donor_in.address,
        city=donor_in.city,
        state=donor_in.state,
        pincode=donor_in.pincode,
        latitude=donor_in.latitude,
        longitude=donor_in.longitude
    )
    db.add(donor)
    db.commit()
    
    # Generate Token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role.value, "user_id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role, "user_id": user.id}

@router.post("/register/ngo", response_model=schemas.Token)
def register_ngo(ngo_in: schemas.NGOCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == ngo_in.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(ngo_in.password)
    user = models.User(email=ngo_in.email, password_hash=hashed_password, role=models.RoleEnum.ngo)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    ngo = models.NGO(
        user_id=user.id,
        ngo_name=ngo_in.ngo_name,
        registration_number=ngo_in.registration_number,
        owner_name=ngo_in.owner_name,
        phone=ngo_in.phone,
        address=ngo_in.address,
        city=ngo_in.city,
        state=ngo_in.state,
        pincode=ngo_in.pincode,
        latitude=ngo_in.latitude,
        longitude=ngo_in.longitude,
        description=ngo_in.description,
        working_areas=ngo_in.working_areas,
        is_verified=False
    )
    db.add(ngo)
    db.commit()
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role.value, "user_id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role, "user_id": user.id}

@router.post("/login", response_model=schemas.Token)
def login(login_data: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == login_data.email).first()
    if not user or not auth.verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role.value, "user_id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role, "user_id": user.id}
