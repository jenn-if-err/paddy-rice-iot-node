import serial
import time

def get_latest_sensor_data(port='/dev/ttyACM0', baudrate=9600, timeout=2):
    """
    Connects to the Arduino via the specified serial port, reads a line of sensor data,
    and returns the parsed values as a list of floats.
    
    Expected data format from Arduino:
        "temperature,humidity,moisture_sensor_value"
        
    Parameters:
        port (str): Serial port where the Arduino is connected (e.g., '/dev/ttyACM0' or '/dev/ttyUSB0').
        baudrate (int): Baud rate for serial communication.
        timeout (int or float): Timeout in seconds for serial read.
        
    Returns:
        list: Sensor values as floats, e.g., [temperature, humidity, moisture_sensor_value],
              or None if no data is read.
    """
    try:
        # Establish the serial connection
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            # Allow time for the connection to initialize
            time.sleep(2)
            # Clear any pre-existing data in the buffer
            ser.flushInput()
            # Read one line from the serial port
            line = ser.readline().decode('utf-8').strip()
            
            if line:
                # Assume the data is comma-separated
                sensor_values = [float(value) for value in line.split(',')]
                return sensor_values
            else:
                print("No data received from Arduino.")
                return None
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return None
    except Exception as e:
        print(f"Error reading sensor data: {e}")
        return None

if __name__ == '__main__':
    # For testing: run this script directly on your Raspberry Pi to see if sensor data is acquired.
    data = get_latest_sensor_data()
    if data:
        print("Acquired sensor data:", data)
    else:
        print("Failed to acquire sensor data.")
