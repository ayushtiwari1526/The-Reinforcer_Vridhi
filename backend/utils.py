import os
import requests

API_KEY = os.getenv("WEATHER_API_KEY", "90e0a81744d44acbad4162121262402")


def get_weather(lat, lon):
    url = "http://api.weatherapi.com/v1/current.json"

    try:
        response = requests.get(
            url,
            params={"key": API_KEY, "q": f"{lat},{lon}"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        return {
            "temperature": None,
            "humidity": None,
            "error": f"Weather service request failed: {str(exc)}",
        }

    current = data.get("current")
    if not current:
        api_error = data.get("error", {}).get("message", "Invalid weather API response")
        return {"temperature": None, "humidity": None, "error": api_error}

    return {
        "temperature": current.get("temp_c"),
        "humidity": current.get("humidity"),
    }
