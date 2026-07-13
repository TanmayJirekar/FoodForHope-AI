from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_food_quality_advice(food_type: str, storage_method: str, preparation_time: str):
    """
    Use Groq API to generate AI advice on food quality and storage.
    """
    if not GROQ_API_KEY or GROQ_API_KEY == "your-groq-api-key":
        return {
            "safety_suggestions": "Keep food refrigerated below 5°C.",
            "storage_suggestions": "Use airtight containers.",
            "shelf_life_recommendations": "Consume within 24 hours."
        }
        
    try:
        client = Groq(api_key=GROQ_API_KEY)
        prompt = f"""
        Act as an AI Food Safety Assistant. 
        I have {food_type} that was prepared at {preparation_time} and is currently stored via {storage_method}.
        Please provide three short bullet points:
        1. Safety Suggestions
        2. Storage Suggestions
        3. Shelf Life Recommendations
        Keep it concise and practical.
        """
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.3,
            max_tokens=200
        )
        
        reply = response.choices[0].message.content
        return {
            "ai_advice": reply
        }
    except Exception as e:
        print(f"Groq API Error: {e}")
        return {
            "ai_advice": "Failed to get AI advice. Ensure food is stored properly."
        }
