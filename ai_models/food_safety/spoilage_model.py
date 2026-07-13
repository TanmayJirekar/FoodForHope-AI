import random
from backend.database.models import FoodSafetyStatus

def analyze_food_safety(image_path: str, food_type: str):
    """
    Mock AI Model for Food Safety Detection.
    In a real scenario, this would use a ResNet50/CNN to analyze the image
    along with the food type to predict spoilage.
    """
    # Simulate processing delay
    # time.sleep(1)
    
    # Generate mock probabilities
    is_safe = random.choice([True, True, True, False]) # 75% chance of being safe for demo
    
    if is_safe:
        score = round(random.uniform(80.0, 99.0), 2)
        if score > 90:
            status = FoodSafetyStatus.safe
            reason = "Food appears fresh and safe for consumption."
        else:
            status = FoodSafetyStatus.moderately_safe
            reason = "Food is safe but should be consumed quickly."
    else:
        score = round(random.uniform(20.0, 79.0), 2)
        if score < 50:
            status = FoodSafetyStatus.spoiled
            reason = "Detected visual signs of spoilage or fungal growth."
        else:
            status = FoodSafetyStatus.unsafe
            reason = "Food appears unsafe or improperly stored."
            
    return {
        "safety_score": score,
        "safety_status": status,
        "safety_reason": reason
    }
