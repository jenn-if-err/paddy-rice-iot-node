import tensorflow as tf
import numpy as np
import joblib

def load_moisture_model():
    """
    Load the pre-trained moisture model saved in .h5 format along with its scaler.
    Adjust the file paths as necessary.
    """
    # Load the Keras model from the .h5 file
    moisture_model = tf.keras.models.load_model(
        'models/moisture_model/model.h5',
        custom_objects={'mean_squared_error': tf.keras.losses.MeanSquaredError()}
    )
    # Load the scaler (which can still be saved with joblib)
    moisture_scaler = joblib.load('models/moisture_model/scaler.joblib')
    return moisture_model, moisture_scaler

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
    # Assuming the model output shape is (1,1)
    return predicted[0][0]

# For testing purposes:
if __name__ == "__main__":
    # Example sensor readings for moisture prediction:
    sample_moisture_data = [50, 25, 60]  # [moisture_sensor_reading, temperature, humidity]
    moisture_content = predict_moisture(sample_moisture_data)
    print("Predicted Moisture Content:", moisture_content)
