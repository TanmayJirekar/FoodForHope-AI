from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from datetime import datetime

from backend.database import database, models
from backend.schemas import schemas
from ai_models.food_safety.spoilage_model import analyze_food_safety
from ai_models.freshness_model.freshness import predict_freshness
from ai_models.ngo_recommender.recommender import recommend_ngos

router = APIRouter()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/create", response_model=schemas.FoodDonationResponse)
async def create_donation(
    donor_id: int = Form(...),
    food_name: str = Form(...),
    food_type: str = Form(...),
    quantity: float = Form(...),
    persons_served: int = Form(...),
    preparation_time: str = Form(...),
    storage_method: str = Form(...),
    storage_temperature: float = Form(...),
    packaging_type: str = Form(...),
    expiry_time: str = Form(...),
    pickup_address: str = Form(...),
    pickup_time: str = Form(...),
    additional_notes: str = Form(""),
    image: UploadFile = File(None),
    db: Session = Depends(database.get_db)
):
    # Process image
    image_url = None
    if image:
        file_location = f"{UPLOAD_DIR}{datetime.now().strftime('%Y%m%d%H%M%S')}_{image.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(image.file, file_object)
        image_url = file_location
        
    # AI Safety Check
    safety_result = analyze_food_safety(image_url if image_url else "", food_type)
    
    if safety_result["safety_status"] in [models.FoodSafetyStatus.spoiled, models.FoodSafetyStatus.unsafe]:
        raise HTTPException(status_code=400, detail=f"Food donation rejected. Reason: {safety_result['safety_reason']}")

    # Freshness Check
    prep_time_dt = datetime.fromisoformat(preparation_time)
    fresh_hours = predict_freshness(food_type, prep_time_dt, storage_temperature)
    
    # Create DB Record
    donation = models.FoodDonation(
        donor_id=donor_id,
        food_name=food_name,
        food_type=food_type,
        quantity=quantity,
        persons_served=persons_served,
        preparation_time=prep_time_dt,
        storage_method=storage_method,
        storage_temperature=storage_temperature,
        packaging_type=packaging_type,
        expiry_time=datetime.fromisoformat(expiry_time),
        pickup_address=pickup_address,
        pickup_time=datetime.fromisoformat(pickup_time),
        additional_notes=additional_notes,
        image_url=image_url,
        safety_score=safety_result["safety_score"],
        safety_status=safety_result["safety_status"],
        safety_reason=safety_result["safety_reason"],
        safe_time_remaining=fresh_hours
    )
    
    db.add(donation)
    db.commit()
    db.refresh(donation)
    
    return donation

@router.get("/donor/{donor_id}", response_model=List[schemas.FoodDonationResponse])
def get_donor_donations(donor_id: int, db: Session = Depends(database.get_db)):
    donations = db.query(models.FoodDonation).filter(models.FoodDonation.donor_id == donor_id).all()
    return donations

@router.get("/ngo/recommendations/{donor_id}/{donation_id}")
def get_ngo_recommendations(donor_id: int, donation_id: int, db: Session = Depends(database.get_db)):
    donor = db.query(models.Donor).filter(models.Donor.id == donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
        
    all_ngos = db.query(models.NGO).all()
    recommendations = recommend_ngos(donor.latitude, donor.longitude, all_ngos)
    
    # Format output
    result = []
    for r in recommendations:
        ngo = r["ngo"]
        result.append({
            "id": ngo.id,
            "ngo_name": ngo.ngo_name,
            "distance_km": r["distance_km"],
            "address": ngo.address,
            "phone": ngo.phone
        })
    return result

@router.post("/assign-ngo/{donation_id}/{ngo_id}")
def assign_ngo(donation_id: int, ngo_id: int, db: Session = Depends(database.get_db)):
    donation = db.query(models.FoodDonation).filter(models.FoodDonation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
        
    donation.ngo_id = ngo_id
    donation.status = models.DonationStatus.accepted
    db.commit()
    return {"message": "Donation assigned successfully"}
