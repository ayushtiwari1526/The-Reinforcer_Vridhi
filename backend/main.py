from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware
from utils import get_weather  #

app = FastAPI()

# Frontend se connect karne ke liye CORS enable karna zaroorat hai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy Database for Farming Guide
crop_guides = {
    "wheat": {
        "name": "Wheat (Gehu)",
        "season": "Rabi",
        "steps": [
            {"day": "1-5", "task": "Soil Preparation", "desc": "Deep plowing and manure addition.", "icon": "fa-mountain", "color": "text-green-500"},
            {"day": "20-25", "task": "First Irrigation", "desc": "Critical stage: Crown Root Initiation.", "icon": "fa-droplet", "color": "text-cyan-400"},
            {"day": "120+", "task": "Harvesting", "desc": "Harvest when grains are hard.", "icon": "fa-wheat-awn", "color": "text-yellow-500"}
        ]
    }
}

@app.get("/api/weather")
async def fetch_weather(lat: float, lon: float):
    # Aapki utils file se real data fetch karega
    return get_weather(lat, lon)

@app.get("/api/guide/{crop_name}")
async def get_guide(crop_name: str):
    return crop_guides.get(crop_name.lower(), {"error": "Guide not found"})

@app.get("/api/dashboard")
async def get_dashboard_data(lat: float, lon: float):
    # 1. Real Weather from your Utils (WeatherAPI)
    weather = get_weather(lat, lon)

    # 2. Live Agri News (Using a free news API or dummy for now)
    news = [
        {"title": "UP Government announces subsidy on solar pumps", "tag": "Govt Scheme"},
        {"title": "Wheat prices expected to rise by 5% in March", "tag": "Market"}
    ]

    # 3. Mandi Rates (Mocking real data structure for Lucknow)
    mandi = [
        {"crop": "Wheat (Gehu)", "price": "2450", "trend": "up"},
        {"crop": "Mustard (Sarson)", "price": "5120", "trend": "down"},
        {"crop": "Potato (Aloo)", "price": "1200", "trend": "stable"}
    ]

    return {
        "weather": weather,
        "news": news,
        "mandi": mandi,
        "location": {"lat": lat, "lon": lon}
    }

# âœ… CORS FIX (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ðŸ” GROQ API KEY
GROQ_API_KEY = "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"

# ðŸŒ¾ CHATBOT API
@app.get("/chat")
def chat(q: str):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "system", "content": "You are a helpful AI farming assistant."},
        {"role": "user", "content": q}
    ]
}

    try:
        response = requests.post(url, headers=headers, json=data)
        res = response.json()

        print(res)  # debug

        # âœ… SAFE RESPONSE HANDLING
        if "choices" in res:
            reply = res["choices"][0]["message"]["content"]
        else:
            reply = "âš ï¸ API Error: " + str(res)

        return {"reply": reply}

    except Exception as e:
        return {"reply": f"âŒ Server Error: {str(e)}"}
