import requests
from datetime import datetime
import os

GENDER = "male"
WEIGHT_KG = "58.5"
HEIGHT_CM = "160"
AGE = "21"

APP_ID = os.environ.get('APP_ID')
API_KEY = os.environ.get('API_KEY')
TOKEN = os.environ.get('TOKEN')
SHEET_ENDPOINT = os.environ.get('SHEET_ENDPOINT')

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

SHEETY_HEADER = {"Authorization": f"Bearer {TOKEN}"}

HEADERS = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

exercise_text = input("Tell me which exercises you did: ")


parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}


response = requests.post(url=exercise_endpoint, json=parameters, headers=HEADERS)
data = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in data["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(url=SHEET_ENDPOINT, json=sheet_inputs, headers=SHEETY_HEADER)
    print(sheet_response.text)