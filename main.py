import machine
import time
import MPU6050
from machine import Pin, PWM
from time import sleep

servo_pin = 28
grad000 = 1638
grad090 = 4915
grad180 = 8192
pwm = PWM(Pin(servo_pin))
pwm.freq(50)

class Vector3:
    def __init__(self, _x, _y, _z):
        self.x = _x
        self.y = _y
        self.z = _z

current = Vector3(0,0,0)

i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1))

mpu = MPU6050.MPU6050(i2c)
mpu.wake()

while True:
    gyro = mpu.read_gyro_data()
    accel = mpu.read_accel_data()
    if gyro[0]/10 >= 1:
        current.x += round(gyro[0]/10,2)
    if gyro[1]/10 >= 1:
        current.y += round(gyro[1]/10,2)
    if gyro[1]/10 >= 1:
        current.z += round(gyro[2]/10,2)
    
    print("x: " + str(current.x) + " y: " + str(current.y) + " z: " + str(current.z))
    if int(current.x/360*8192) > 8192:
        current.x = 0
    pwm.duty_u16(int(current.x/360*8192))
    time.sleep(0.1)