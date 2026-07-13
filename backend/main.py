from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from backend.database import database, models
from backend.api import auth_routes, donation_routes

load_dotenv()

# Auto-create the database if it doesn't exist
try:
    db_url = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:root@localhost:3306/foodforhope")
    base_url = db_url.rsplit('/', 1)[0]
    db_name = db_url.rsplit('/', 1)[1]
    
    engine_temp = create_engine(base_url)
    with engine_temp.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
        conn.commit()
    print(f"Database {db_name} checked/created successfully.")
except Exception as e:
    print(f"Warning: Could not auto-create database {db_name}. Error: {e}")

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="FoodForHope AI", description="Smart Food Donation Platform API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(donation_routes.router, prefix="/api/donations", tags=["Donations"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FoodForHope AI API"}
