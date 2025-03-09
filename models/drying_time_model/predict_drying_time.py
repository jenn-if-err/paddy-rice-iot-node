import joblib
import numpy as np
from pathlib import Path

# Automatically determine the base directory of the script
BASE_DIR = Path(__file__).resolve().parent

# Define model and scaler paths dynamically
MODEL_PATH = BASE_DIR / "drying_time_rf_model.joblib"
SCALER_PATH = BASE_DIR / "drying_time_rf_scaler.joblib"

try:
    drying_model = joblib.load(MODEL_PATH)
    drying_scaler = joblib.load(SCALER_PATH)
except Exception as e:
    print(f"Error loading model: {e}")
    drying_model = None
    drying_scaler = None

def predict_drying_time(initial_moisture, temperature, humidity, final_moisture):
    """
    Predict drying time using the trained drying time model.

    Parameters:
        initial_moisture (float): Moisture content obtained from the moisture model.
        temperature (float): Temperature reading from the DHT sensor.
        humidity (float): Humidity reading from the DHT sensor.
        final_moisture (float): Desired final moisture content.

    Returns:
        float: Predicted drying time.
    """
    if drying_model is None or drying_scaler is None:
        raise ValueError("Model or scaler not loaded properly.")

    # Combine the features in the correct order
    input_features = np.array([[initial_moisture, temperature, humidity, final_moisture]])

    # Scale the input features
    input_scaled = drying_scaler.transform(input_features)

    # Predict drying time
    predicted_time = drying_model.predict(input_scaled)
    
    return predicted_time[0]
