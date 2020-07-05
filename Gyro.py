from Kalman import KalmanAngle
import board
import time
import math
import adafruit_lsm9ds1

kalmanX = KalmanAngle()
kalmanY = KalmanAngle()

RestrictPitch = True  # Comment out to restrict roll to ±90deg instead - please read: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf
radToDeg = 57.2957786


# Read the gyro and acceleromater values from MPU6050
class Gyro:
    def __init__(self):
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
            time.sleep(1)
        except:
            self.sensor = None
            print("No gyro connected")

    def get_x_degrees(self):
        if self.sensor is None:
            return None
        else:
            kalAngleX = 0
            kalAngleY = 0

            accX, accX, accZ = self.sensor.acceleration

            # print(accX,accY,accZ)
            # print(math.sqrt((accY**2)+(accZ**2)))
            if (RestrictPitch):
                roll = math.atan2(accY, accZ) * radToDeg
                pitch = math.atan(-accX / math.sqrt((accY ** 2) + (accZ ** 2))) * radToDeg
            else:
                roll = math.atan(accY / math.sqrt((accX ** 2) + (accZ ** 2))) * radToDeg
                pitch = math.atan2(-accX, accZ) * radToDeg

            kalmanX.setAngle(roll)
            kalmanY.setAngle(pitch)
            gyroXAngle = roll;
            gyroYAngle = pitch;
            compAngleX = roll;
            compAngleY = pitch;

            timer = time.time()
            flag = 0
            while flag < 100:
                try:
                    # Read Accelerometer raw value
                    accX, accX, accZ = self.sensor.acceleration

                    # Read Gyroscope raw value
                    gyroX, gyroY, gyroZ = self.sensor.gyro

                    dt = time.time() - timer
                    timer = time.time()

                    if (RestrictPitch):
                        roll = math.atan2(accY, accZ) * radToDeg
                        pitch = math.atan(-accX / math.sqrt((accY ** 2) + (accZ ** 2))) * radToDeg
                    else:
                        roll = math.atan(accY / math.sqrt((accX ** 2) + (accZ ** 2))) * radToDeg
                        pitch = math.atan2(-accX, accZ) * radToDeg

                    gyroXRate = gyroX / 131
                    gyroYRate = gyroY / 131

                    if RestrictPitch:

                        if (roll < -90 and kalAngleX > 90) or (roll > 90 and kalAngleX < -90):
                            kalmanX.setAngle(roll)
                            complAngleX = roll
                            kalAngleX = roll
                            gyroXAngle = roll
                        else:
                            kalAngleX = kalmanX.getAngle(roll, gyroXRate, dt)
                        if abs(kalAngleX) > 90:
                            gyroYRate = -gyroYRate
                            kalAngleY = kalmanY.getAngle(pitch, gyroYRate, dt)
                    else:

                        if (pitch < -90 and kalAngleY > 90) or (pitch > 90 and kalAngleY < -90):
                            kalmanY.setAngle(pitch)
                            complAngleY = pitch
                            kalAngleY = pitch
                            gyroYAngle = pitch
                        else:
                            kalAngleY = kalmanY.getAngle(pitch, gyroYRate, dt)

                        if (abs(kalAngleY) > 90):
                            gyroXRate = -gyroXRate
                            kalAngleX = kalmanX.getAngle(roll, gyroXRate, dt)

                    gyroXAngle = gyroXRate * dt
                    gyroYAngle = gyroYAngle * dt

                    compAngleX = 0.93 * (compAngleX + gyroXRate * dt) + 0.07 * roll
                    compAngleY = 0.93 * (compAngleY + gyroYRate * dt) + 0.07 * pitch

                    if (gyroXAngle < -180) or (gyroXAngle > 180):
                        gyroXAngle = kalAngleX
                    if (gyroYAngle < -180) or (gyroYAngle > 180):
                        gyroYAngle = kalAngleY

                    return round(gyroXAngle, 2);

                except Exception as exc:
                    print(exc)
                    flag += 1
            print("There is a problem with the gyro connection")
            return None

    def get_temperature(self):
        if self.sensor is None:
            return None
        else:
            temp = self.sensor.temperature
            return round(temp, 1)
