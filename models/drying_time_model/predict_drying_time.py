import joblib
import numpy as np

def load_drying_time_model():
    """
    Load the pre-trained drying time model and its scaler.
    Adjust the file paths as necessary.
    """
    drying_model = joblib.load('models/drying_time_model/drying_time_rf_model.joblib')
    drying_scaler = joblib.load('models/drying_time_model/drying_time_rf_scaler.joblib')
    return drying_model, drying_scaler

def predict_drying_time(sensor_data, sample_moisture, mc_final):
    """
    Predict drying time using the drying time model.
    
    Parameters:
        sensor_data (list or array): Sensor readings from the DHT sensor, e.g., [temperature, humidity].
        sample_moisture (float): Moisture content obtained from the moisture model (initial moisture).
        mc_final (float): Final moisture content measurement.
        
    Returns:
        float: Predicted drying time.
    """
    model, scaler = load_drying_time_model()
    
    # Combine the features into a single array:
    # Order: [sample_moisture, temperature, humidity, mc_final]
    combined_features = np.array([sample_moisture] + sensor_data + [mc_final]).reshape(1, -1)
    
    # Scale the features using the loaded scaler
    combined_features_scaled = scaler.transform(combined_features)
    
    # Make the prediction
    predicted_time = model.predict(combined_features_scaled)
    return predicted_time[0]

# For testing purposes: simple command line execution.
if __name__ == "__main__":
    # Example sensor readings (temperature and humidity)
    sample_sensor_data = [30, 70]  # [temperature, humidity]
    
    # Example values:
    sample_moisture = 18.5  # Moisture content from the moisture model (initial moisture)
    sample_mc_final = 12.5  # Final moisture content measurement
    
    drying_time = predict_drying_time(sample_sensor_data, sample_moisture, sample_mc_final)
    print("Predicted Drying Time:", drying_time)
