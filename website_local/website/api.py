import requests
from flask import session
from flask import Blueprint

api = Blueprint('api', __name__)

REMOTE_URL = "https://paddy-rice-tracker.onrender.com"

def authenticate_user(username, password):
    LOGIN_ENDPOINT = f"{REMOTE_URL}/login"
    response = requests.post(LOGIN_ENDPOINT, data={"username": username, "password": password})
    if response.status_code == 200:
        session.permanent = True
        session['token'] = response.json().get('token')
        return True
    return False

def fetch_farmer_data(username):
    FARMER_ENDPOINT = f"{REMOTE_URL}/api/farmers/{username}"
    headers = {"Authorization": f"Bearer {session.get('token')}"}
    response = requests.get(FARMER_ENDPOINT, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_user_data():
    USER_ENDPOINT = f"{REMOTE_URL}/api/users"
    response = requests.get(USER_ENDPOINT)

    print("USER_ENDPOINT status:", response.status_code)
    print("USER_ENDPOINT response text:", response.text)

    if response.status_code == 200:
        try:
            return response.json()  
        except Exception as e:
            print(" JSON decode error:", e)
            return []
    else:
        print("Failed to fetch users:", response.status_code)
        return []

def fetch_barangay_data():
    BARANGAY_ENDPOINT = f"{REMOTE_URL}/api/barangays"
    response = requests.get(BARANGAY_ENDPOINT)

    print("BARANGAY_ENDPOINT status:", response.status_code)
    print("BARANGAY_ENDPOINT response text:", response.text)

    if response.status_code == 200:
        try:
            return response.json() 
        except Exception as e:
            print("JSON decode error:", e)
            return []
    else:
        print("Failed to fetch barangays:", response.status_code)
        return []

def fetch_municipality_data():
    MUNICIPALITY_ENDPOINT = f"{REMOTE_URL}/api/municipalities"
    response = requests.get(MUNICIPALITY_ENDPOINT)

    print("MUNICIPALITY_ENDPOINT status:", response.status_code)
    print("MUNICIPALITY_ENDPOINT response text:", response.text)

    if response.status_code == 200:
        try:
            return response.json()  
        except Exception as e:
            print("JSON decode error:", e)
            return []
    else:
        print("Failed to fetch municipalities:", response.status_code)
        return []
