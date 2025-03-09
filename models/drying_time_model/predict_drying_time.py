from pathlib import Path
import joblib
import numpy as np

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

def predict_drying_time(sensor_data, sample_moisture, mc_final):
    """
    Predict drying time using the drying time model.
    """
    model, scaler = load_drying_time_model()
    combined_features = np.array([sample_moisture] + sensor_data + [mc_final]).reshape(1, -1)
    combined_features_scaled = scaler.transform(combined_features)
    predicted_time = model.predict(combined_features_scaled)
    return predicted_time[0]

if __name__ == "__main__":
    sample_sensor_data = [30, 70]  
    sample_moisture = 18.5  
    sample_mc_final = 12.5  
    drying_time = predict_drying_time(sample_sensor_data, sample_moisture, sample_mc_final)
    print("Predicted Drying Time:", drying_time)
