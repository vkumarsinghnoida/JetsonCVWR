import serial
import time

# Define the serial port and baud rate
ser = serial.Serial('/dev/ttyACM0', 9600)  # Update the port as needed

def control_led(led1, led2, brightness):
    # Format the command as "L1:on,L2:on,B:xxx"
    command = f"L1:{led1},L2:{led2},B:{brightness}"
    ser.write(command.encode())
    print(f"Sent command: {command}")

try:
    while True:
        led1_state = input("Enter LED 1 state (on/off): ").lower()
        led2_state = input("Enter LED 2 state (on/off): ").lower()
        brightness = int(input("Enter LED brightness (0-180): "))

        if led1_state not in ["on", "off"] or led2_state not in ["on", "off"] or brightness < 0 or brightness > 180:
            print("Invalid input. LED states must be 'on' or 'off', brightness between 0 and 180.")
            continue

        control_led(led1_state, led2_state, brightness)
        time.sleep(1)  # Optional delay between commands

except KeyboardInterrupt:
    print("\nExiting the program.")
    ser.close()

