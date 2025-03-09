import sys
from models.drying_time_model.predict_drying_time import predict_drying_time
from models.moisture_model.predict_moisture import predict_moisture


def show_temperature():

    temperature=30

    return temperature

def show_humidity():

    humidity=70

    return humidity

def show_initial_moisture():
    """
    Predict moisture content using predefined sample sensor readings.
    
    Returns:
        float: Predicted moisture content.
    """

    initial_moisture = 18.5  
    return initial_moisture
    
def receive_final_moisture():

    final_moisture= 12.5

    return final_moisture 

def show_drying_time():
    """
    Predict drying time using predefined sample sensor readings.
    
    Returns:
        float: Predicted drying time.
    """
    
    
    # Predict drying time
    drying_time = predict_drying_time(show_temperature, show_humidity, show_initial_moisture, receive_final_moisture)
    return drying_time

if __name__ == "__main__":
    drying_time = predict_drying_time()
    print("Predicted Drying Time:", drying_time)
