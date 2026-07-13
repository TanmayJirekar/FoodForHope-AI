def predict_freshness(food_type: str, preparation_time, storage_temp: float):
    """
    Mock AI Model for Food Freshness Predictor.
    Predicts how many hours the food will remain safe.
    """
    base_hours = {
        "Cooked Food": 6,
        "Packed Food": 48,
        "Vegetables": 72,
        "Fruits": 72,
        "Bakery": 24,
        "Milk Products": 12,
        "Dry Food": 720
    }
    
    hours = base_hours.get(food_type, 12)
    
    # Adjust based on temperature
    if storage_temp < 5:
        hours *= 2  # Refrigerated
    elif storage_temp > 25:
        hours *= 0.5 # Hot room temp
        
    return round(hours, 1)
