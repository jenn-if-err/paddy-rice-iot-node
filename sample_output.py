import sys
from models.drying_time_model.predict_drying_time import predict_drying_time
from models.moisture_model.predict_moisture import predict_moisture


def predict_sample_drying_time():
    """
    Predict drying time using predefined sample sensor readings.
    
    Returns:
        float: Predicted drying time.
    """
    # Example sensor readings (temperature and humidity)
    sample_sensor_data = [30, 70]  # [temperature, humidity]
    
    # Example values:
    sample_moisture = 18.5  # Moisture content from the moisture model (initial moisture)
    sample_mc_final = 12.5  # Final moisture content measurement
    
    # Predict drying time
    drying_time = predict_drying_time(sample_sensor_data, sample_moisture, sample_mc_final)
    return drying_time

if __name__ == "__main__":
    drying_time = predict_sample_drying_time()
    print("Predicted Drying Time:", drying_time)
