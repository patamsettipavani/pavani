import requests

# Mee token ni ikkada paste cheyandi (Register/Login response lo vachina)
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc4ODg3NjUzMywianRpIjoiZTM3NzIxODktYmJlYi00MTNmLTk5YWYtNGMxOTY0NDk2YmI4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjUiLCJuYmYiOjE3ODg4NzY1MzMsImNzcmYiOiI5MTgxZTRmZi05OTY0LTRhYzYtOGE1MC05ZDdiZmNiMzI3ODUiLCJleHAiOjE3ODg4Nzc0MzN9.BssO6mqWE47sT-QpqdjCItqHvO7XTPAdtOkGj5HZfC4"

# Mee PDF file path ni ikkada paste cheyandi (Step 1 lo copy chesina path)
PDF_PATH = r"C:\Users\User\Desktop\Desktop\Resume_Varaprasad_Bsc comp.pdf"  # <-- Mee correct path ni ikkada pettandi

url = "http://localhost:5000/api/upload-resume"
headers = {"Authorization": f"Bearer {TOKEN}"}

print(f"Uploading: {PDF_PATH}")

with open(PDF_PATH, "rb") as f:
    files = {"file": f}
    response = requests.post(url, headers=headers, files=files)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")