import matplotlib.pyplot as plt
import serial
import time

# Serial port configuration for Arduino Mega
arduino_port = 'COM7'  
baud_rate = 9600

# Establish serial communication
ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(1)  # Wait for the serial connection to initialize

# Function to read potentiometer value from Arduino
def read_potentiometer():
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()  # Read line from serial, decode, and strip whitespace
        try:
            return int(data)  # Convert reading to integer
        except ValueError:
            return None  # In case of an invalid reading
    return None

# Initialize plot
plt.ion()  # Enable interactive mode
fig, ax = plt.subplots()
readings = []
num_readings = 50  # Number of readings to display on the plot
line, = ax.plot(readings, label="Potentiometer Reading")
ax.set_ylim(0, 1023)  # Set y-axis range for Arduino analog values (0 to 1023)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Potentiometer Reading")
plt.title("Real-time Potentiometer Readings from Arduino")
plt.legend()

# Function to update the plot
def update_plot():
    line.set_ydata(readings)
    line.set_xdata(range(len(readings)))
    ax.relim()  # Recalculate limits
    ax.autoscale_view()  # Rescale to fit new data
    plt.draw()
    plt.pause(0.1)

# Main loop for reading data and updating plot
try:
    for i in range(num_readings * 2):  # Adjust this for desired duration
        reading = read_potentiometer()
        
        if reading is not None:
            readings.append(reading)
            
            # Keep the latest readings only
            if len(readings) > num_readings:
                readings.pop(0)
            
            # Update the plot
            update_plot()
        
            time.sleep(0.1)# Match Arduino's delay

except KeyboardInterrupt:
    print("Data collection stopped by user.")

finally:
    ser.close()  # Close serial connection
    plt.ioff()   # Turn off interactive mode
    plt.show()
