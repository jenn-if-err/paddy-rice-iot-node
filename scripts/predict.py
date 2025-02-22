import joblib
import numpy as np

def load_moisture_model():
    """
    Load the pre-trained moisture model and its scaler.
    Adjust the file paths as necessary.
    """
    moisture_model = joblib.load('models/moisture_model/model.joblib')
    moisture_scaler = joblib.load('models/moisture_model/scaler.joblib')
    return moisture_model, moisture_scaler

def load_drying_time_model():
    """
    Load the pre-trained drying time model and its scaler.
    Adjust the file paths as necessary.
    """
    drying_model = joblib.load('models/drying_time_model/model_v10.joblib')
    drying_scaler = joblib.load('models/drying_time_model/scaler_v10.joblib')
    return drying_model, drying_scaler

def predict_moisture(sensor_data):
    """
    Predict moisture content using the moisture model.
    
    Parameters:
        sensor_data (list or array): Input features for the moisture model.
            For example, this could be [moisture_sensor_reading, temperature, humidity]
            if that is what your model was trained on.
    
    Returns:
        float: Predicted moisture content.
    """
    model, scaler = load_moisture_model()
    # Ensure sensor_data is in the proper shape (1, number_of_features)
    features = np.array(sensor_data).reshape(1, -1)
    features_scaled = scaler.transform(features)
    predicted = model.predict(features_scaled)
    return predicted[0]

def predict_drying_time(sensor_data, predicted_moisture):
    """
    Predict drying time using the drying time model.
    
    Parameters:
        sensor_data (list or array): Input features from the DHT sensor,
            e.g., [temperature, humidity]
        predicted_moisture (float): Moisture content obtained from the moisture model.
        
    Returns:
        float: Predicted drying time.
    """
    model, scaler = load_drying_time_model()
    # Combine the sensor_data with the predicted moisture content.
    # Assume the model was trained on features in the order: [temperature, humidity, moisture_content]
    combined_features = np.array(sensor_data + [predicted_moisture]).reshape(1, -1)
    combined_features_scaled = scaler.transform(combined_features)
    predicted_time = model.predict(combined_features_scaled)
    return predicted_time[0]

# For testing purposes: simple command line execution.
if __name__ == "__main__":
    # Example sensor readings for moisture prediction:
    # (Replace these with real sensor values or test values as appropriate.)
    # Example: [moisture_sensor_reading, temperature, humidity]
    sample_moisture_data = [50, 25, 60]
    moisture_content = predict_moisture(sample_moisture_data)
    print("Predicted Moisture Content:", moisture_content)

    # For drying time prediction, assume sensor data: [temperature, humidity]
    sample_drying_data = [25, 60]
    drying_time = predict_drying_time(sample_drying_data, moisture_content)
    print("Predicted Drying Time:", drying_time)
