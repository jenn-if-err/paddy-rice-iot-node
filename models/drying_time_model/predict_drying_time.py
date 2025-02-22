import joblib
import numpy as np

def load_drying_time_model():
    """
    Load the pre-trained drying time model and its scaler.

    """
    drying_model = joblib.load('drying_time_rf_model.joblib')
    drying_scaler = joblib.load('drying_time_rf_scaler.joblib')
    return drying_model, drying_scaler

def predict_drying_time(sensor_data, predicted_moisture):
    """
    Predict drying time using the drying time model.
    
    Parameters:
        sensor_data (list or array): Input features from the DHT sensor,
            e.g., [temperature, humidity].
        predicted_moisture (float): Moisture content obtained from the moisture model.
        
    Returns:
        float: Predicted drying time.
    """
    model, scaler = load_drying_time_model()
    
    # Combine sensor_data with the predicted moisture content.
    # Here we assume the model was trained on features in the order:
    # [temperature, humidity, moisture_content]
    combined_features = np.array(sensor_data + [predicted_moisture]).reshape(1, -1)
    
    # Scale the features using the loaded scaler
    combined_features_scaled = scaler.transform(combined_features)
    
    # Make the prediction
    predicted_time = model.predict(combined_features_scaled)
    return predicted_time[0]

# For testing purposes: simple command line execution.
if __name__ == "__main__":
    # Example sensor readings for drying time prediction:
    # [temperature, humidity]
    sample_drying_data = [25, 60]
    
    # Example predicted moisture content (from the moisture model)
    sample_moisture = 50.0
    
    drying_time = predict_drying_time(sample_drying_data, sample_moisture)
    print("Predicted Drying Time:", drying_time)
