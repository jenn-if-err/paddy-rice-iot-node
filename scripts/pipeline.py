import time
from predict import predict_moisture, predict_drying_time

def get_sensor_data():
    """
    Acquire sensor data.
    In a production system, replace this with code that reads data from the Arduino.
    
    Returns:
        list: [moisture_sensor_reading, temperature, humidity]
    """
    print("Acquiring sensor data...")
    try:
        moisture_sensor_value = float(input("Enter moisture sensor reading: "))
        temperature = float(input("Enter temperature: "))
        humidity = float(input("Enter humidity: "))
    except ValueError:
        print("Invalid input. Using default dummy values.")
        moisture_sensor_value, temperature, humidity = 50.0, 25.0, 60.0
    return [moisture_sensor_value, temperature, humidity]

def main():
    print("Pipeline started.")
    
    # Step 1: Wait for the user to press "Read"
    input("Press Enter to 'Read' sensor data...")
    
    # Data Acquisition: Get sensor readings
    sensor_data = get_sensor_data()
    print("Sensor data acquired:", sensor_data)
    
    # Step 2: Predict moisture content using the moisture model saved as .h5.
    # This function loads the model (using tf.keras.models.load_model) and the scaler.
    predicted_moisture = predict_moisture(sensor_data)
    print("Predicted Moisture Content:", predicted_moisture)
    
    # In a production setup, you might display the moisture content on the web app or update a database.
    
    # Step 3: Wait for the user to press "Predict" for drying time
    input("Press Enter to 'Predict' drying time...")
    
    # For drying time prediction, the model uses [temperature, humidity, predicted_moisture]
    drying_sensor_data = sensor_data[1:]  # [temperature, humidity]
    predicted_drying_time = predict_drying_time(drying_sensor_data, predicted_moisture)
    print("Predicted Drying Time:", predicted_drying_time)
    
    # Optionally, update a database or file so that your web app can display the results.
    
if __name__ == '__main__':
    main()
