import requests
from flask import session

REMOTE_URL = "http://localhost:5001"

def authenticate_user(username, password):
    LOGIN_ENDPOINT = f"{REMOTE_URL}/login"
    response = requests.post(LOGIN_ENDPOINT, data={"username": username, "password": password})
    if response.status_code == 200:
        session['token'] = response.json().get('token')  # Store token for future requests
        return True
    return False

def fetch_farmer_data(username):
    FARMER_ENDPOINT = f"{REMOTE_URL}/api/farmers/{username}"
    headers = {"Authorization": f"Bearer {session.get('token')}"}
    response = requests.get(FARMER_ENDPOINT, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_related_data():
    BARANGAY_ENDPOINT = f"{REMOTE_URL}/api/barangays"
    MUNICIPALITY_ENDPOINT = f"{REMOTE_URL}/api/municipalities"
    headers = {"Authorization": f"Bearer {session.get('token')}"}

    barangay_response = requests.get(BARANGAY_ENDPOINT, headers=headers)
    municipality_response = requests.get(MUNICIPALITY_ENDPOINT, headers=headers)

    if barangay_response.status_code == 200 and municipality_response.status_code == 200:
        barangays = barangay_response.json()
        municipalities = municipality_response.json()
        return barangays, municipalities
    return None, None
