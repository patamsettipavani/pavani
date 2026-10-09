import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

try:
    genai.configure(api_key=api_key)
    
    print("✅ Available Gemini Models:\n")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  • {model.name}")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")