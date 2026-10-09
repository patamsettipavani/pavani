import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

print(f"Testing API Key: {api_key[:20]}...")
print(f"Model: {model_name}")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Say 'Hello' in one word")
    print(f"\n✅ SUCCESS! Response: {response.text}")
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")