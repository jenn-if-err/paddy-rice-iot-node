import sys
from models.drying_time_model.predict_drying_time import predict_drying_time
from models.moisture_model.predict_moisture import predict_moisture

def show_capacitive():

    capacitive=30

    return capacitive

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
    capacitive=show_capacitive()
    temperature = show_temperature()
    humidity = show_humidity()
    initial_moisture = predict_moisture(capacitive, temperature, humidity)
    #initial_moisture = 18.5  
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
    temperature = show_temperature()
    humidity = show_humidity()
    initial_moisture = show_initial_moisture()
    final_moisture = receive_final_moisture()
    
    drying_time = predict_drying_time(initial_moisture, temperature, humidity, final_moisture)
    return drying_time

if __name__ == "__main__":
    drying_time = show_drying_time()
    print("Predicted Drying Time:", drying_time)
