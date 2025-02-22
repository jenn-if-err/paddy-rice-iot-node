import time
from predict import predict_moisture, predict_drying_time

def get_sensor_data():
    """
    Simulate sensor data acquisition.
    In a production system, replace this with actual code to read data from the Arduino.
    
    Returns:
        list: [moisture_sensor_reading, temperature, humidity]
    """
    print("Acquiring sensor data...")
    # For simulation, you can either input values or generate dummy data.
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
    
    # Step 2: Predict moisture content using the moisture model
    # The moisture model expects all three values: [moisture_sensor_reading, temperature, humidity]
    predicted_moisture = predict_moisture(sensor_data)
    print("Predicted Moisture Content:", predicted_moisture)
    
    # Display the moisture content (e.g., on the web app)
    # In production, this result might be sent to a database or API for the web interface.
    
    # Step 3: Wait for the user to press "Predict" for drying time
    input("Press Enter to 'Predict' drying time...")
    
    # For drying time, the model is trained on [temperature, humidity, predicted_moisture]
    drying_sensor_data = sensor_data[1:]  # [temperature, humidity]
    predicted_drying_time = predict_drying_time(drying_sensor_data, predicted_moisture)
    print("Predicted Drying Time:", predicted_drying_time)
    
    # In a full implementation, you could update a database or file here so that your web app can display the results.
    
if __name__ == '__main__':
    main()
