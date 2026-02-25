import requests
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse

app = FastAPI()

def get_ip_info(ip_address):
    
    base = Path(__file__).resolve().parent.parent  # project root
    env_path = base / ".env"
    load_dotenv(dotenv_path=str(env_path))
    API_KEY = os.getenv("IPGEO_API_KEY")
    headers = {}
    url = f"https://api.ipgeolocation.io/v3/ipgeo?apiKey={API_KEY}&ip={ip_address}"
    response = requests.request("GET", url, headers=headers, data={})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

@app.get("/", response_class=PlainTextResponse)
def ip_info(ip: str = Query(..., description="IP Address")):
    info = get_ip_info(ip)
    if info is None:
        return("IP information not found")
    country_name = info["location"]["country_name"]
    city_name = info["location"]["city"]
    return f"{country_name}/{city_name}"