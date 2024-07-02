# SG90 and MPU-6050 with the RaspberryPi Zero.
A simple python programm that controlls the servo when the gyrosensor is turned in the x axis.

## Setup
1. Connect the VCC of the MPU-6050 to the 3v3 pin on the pico, as well as the GND pin to GND on the pico. After that, connect SCL to GP1 and SDA to GP0.
2. Connect the Red wire of the SG90 to VBUS and the brown wire of the SG90 to GND. Connect the remaining wire (yellow/orange wire) to GP28_A2 on the pico.
3. Download the code from the repository and upload both files to the RaspberryPi Pico with Thonny.
4. The MPU-6050 is connected correctly, if the green LED is on.

## How the code works
#### Importing the libraries
```python
import machine
import time
import MPU6050
from machine import Pin, PWM
from time import sleep
```

#### Declaring the variables
```python
servo_pin = 28
grad000 = 1638
grad090 = 4915
grad180 = 8192
pwm = PWM(Pin(servo_pin))
pwm.freq(50)
```

#### Making a class to store the rotation
```python
class Vector3:
    def __init__(self, _x, _y, _z):
        self.x = _x
        self.y = _y
        self.z = _z

current = Vector3(0,0,0)
```

#### Connecting to the MPU
```python
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1))
mpu = MPU6050.MPU6050(i2c)
mpu.wake()
```

#### Main Loop
```python
while True:
    gyro = mpu.read_gyro_data() # Stores the gyro data in a variable.
    accel = mpu.read_accel_data() # Stores the acceleration data in a variable.

    # Short code the ensure a deadzone
    if gyro[0]/10 >= 1:
        current.x += round(gyro[0]/10,2)
    if gyro[1]/10 >= 1:
        current.y += round(gyro[1]/10,2)
    if gyro[1]/10 >= 1:
        current.z += round(gyro[2]/10,2)

    # Log the data to the console.
    print("x: " + str(current.x) + " y: " + str(current.y) + " z: " + str(current.z))

    # Normalizing the data to convert it into the servo motor units.
    if int(current.x/360*8192) > 8192:
        current.x = 0
    pwm.duty_u16(int(current.x/360*8192))
    time.sleep(0.1)
```
