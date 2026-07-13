def predict_impact(quantity_kg: float, food_type: str):
    """
    Mock AI Model to predict how many people can be fed.
    Average meal is roughly 0.4 kg.
    """
    base_multiplier = 2.5 # people per kg
    
    if food_type == "Dry Food":
        base_multiplier = 4.0 # Rice/Dal expands when cooked
    elif food_type == "Vegetables":
        base_multiplier = 3.0
        
    estimated_people = int(quantity_kg * base_multiplier)
    return estimated_people
