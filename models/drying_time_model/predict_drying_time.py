from pathlib import Path
import joblib
import numpy as np
import pandas as pd

# Automatically find the base directory of the script
BASE_DIR = Path(__file__).resolve().parent

# Model paths relative to this script's location
MODEL_PATH = BASE_DIR / "drying_time_rf_model.joblib"
SCALER_PATH = BASE_DIR / "drying_time_rf_scaler.joblib"

def load_drying_time_model():
    """
    Load the pre-trained drying time model and its scaler.
    """
    drying_model = joblib.load(MODEL_PATH)
    drying_scaler = joblib.load(SCALER_PATH)
    return drying_model, drying_scaler


def predict_drying_time(temperature, humidity, mc_initial, mc_final):
    """
    Predict drying time using the drying time model.
    """
    model, scaler = load_drying_time_model()

    # Define the expected feature names (from when StandardScaler was trained)
    feature_names = ["mc_initial", "temperature", "humidity", "mc_final"]

    # Convert the input array into a DataFrame with proper column names
    combined_features_df = pd.DataFrame([mc_initial] + sensor_data + [mc_final], 
                                        index=feature_names).T  # Transpose to match (1, n_features)

    # Scale the features using the loaded scaler
    combined_features_scaled = scaler.transform(combined_features_df)

    # Make the prediction
    predicted_time = model.predict(combined_features_scaled)
    return predicted_time[0]


if __name__ == "__main__":
    sample_sensor_data = [30, 70]  
    sample_moisture = 18.5  
    sample_mc_final = 12.5  
    drying_time = predict_drying_time(sample_sensor_data, sample_moisture, sample_mc_final)
    print("Predicted Drying Time:", drying_time)
