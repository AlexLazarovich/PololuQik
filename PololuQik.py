from gpiozero import DigitalOutputDevice, DigitalInputDevice
from serial import Serial

QIK_GET_FIRMWARE_VERSION =          0x81
QIK_GET_ERROR_BYTE =                0x82
QIK_GET_CONFIGURATION_PARAMETER =   0x83
QIK_SET_CONFIGURATION_PARAMETER =   0x84

QIK_MOTOR_M0_FORWARD =              0x88
QIK_MOTOR_M0_FORWARD_8_BIT =        0x89
QIK_MOTOR_M0_REVERSE =              0x8A
QIK_MOTOR_M0_REVERSE_8_BIT =        0x8B
QIK_MOTOR_M1_FORWARD =              0x8C
QIK_MOTOR_M1_FORWARD_8_BIT =        0x8D
QIK_MOTOR_M1_REVERSE =              0x8E
QIK_MOTOR_M1_REVERSE_8_BIT =        0x8F

# 2s9v1 only
QIK_2S9V1_MOTOR_M0_COAST =          0x86
QIK_2S9V1_MOTOR_M1_COAST =          0x87

# 2s12v10 only
QIK_2S12V10_MOTOR_M0_BRAKE =        0x86
QIK_2S12V10_MOTOR_M1_BRAKE =        0x87
QIK_2S12V10_GET_MOTOR_M0_CURRENT =  0x90
QIK_2S12V10_GET_MOTOR_M1_CURRENT =  0x91
QIK_2S12V10_GET_MOTOR_M0_SPEED =    0x92
QIK_2S12V10_GET_MOTOR_M1_SPEED =    0x93

# Configuration parameters

QIK_CONFIG_DEVICE_ID =                          0
QIK_CONFIG_PWM_PARAMETER =                      1
QIK_CONFIG_SHUT_DOWN_MOTORS_ON_ERROR =          2
QIK_CONFIG_SERIAL_TIMEOUT =                     3
QIK_CONFIG_MOTOR_M0_ACCELERATION =              4
QIK_CONFIG_MOTOR_M1_ACCELERATION =              5
QIK_CONFIG_MOTOR_M0_BRAKE_DURATION =            6
QIK_CONFIG_MOTOR_M1_BRAKE_DURATION =            7
QIK_CONFIG_MOTOR_M0_CURRENT_LIMIT_DIV_2 =       8
QIK_CONFIG_MOTOR_M1_CURRENT_LIMIT_DIV_2 =       9
QIK_CONFIG_MOTOR_M0_CURRENT_LIMIT_RESPONSE =    10
QIK_CONFIG_MOTOR_M1_CURRENT_LIMIT_RESPONSE =    11


class PololuQik(Serial):
    def __init__(self, port, resetPin, speed = 9600):
        super().__init__(port = port, baudrate = speed)

        DigitalOutputDevice(pin = resetPin, initial_value = False)
        self._resetOut = DigitalInputDevice(pin = resetPin)
        self.open()
        self.write(0xAA)

    def write(self, data):
        if type(data) != tuple:
            return super().write(data)
        for seg in data:
            yield super().write(seg)

    def getFirmwareVersion(self):
        #self.listen()
        self.write(QIK_GET_FIRMWARE_VERSION)
        #while (self.available() < 1):
        #    pass
        return self.read()

    def getErrors(self):
        #self.listen()
        self.write(QIK_GET_ERROR_BYTE)
        #while (self.available() < 1):
        #    pass
        return self.read()

    def getConfigurationParameter(self, parameter):
        #self.listen()
        cmd = QIK_GET_CONFIGURATION_PARAMETER, parameter
        self.write(cmd)
        #while (self.available() < 1):
        #    pass
        return self.read()

    def setConfigurationParameter(self, parameter, value):
        #self.listen()
        cmd = QIK_SET_CONFIGURATION_PARAMETER, parameter, value, 0x55, 0x2A
        self.write(cmd)
        #while (self.available() < 1):
        #    pass
        return self.read()

    def setM0Speed(self, speed):
        reverse = False

        if (speed < 0):
            speed = -speed; # make speed a positive quantity
            reverse = True; # preserve the direction
        if (speed > 255):
            speed = 255

        if (speed > 127):
            # 8-bit mode: actual speed is (speed + 128)
            cmd = QIK_MOTOR_M0_REVERSE_8_BIT if reverse else QIK_MOTOR_M0_FORWARD_8_BIT, speed - 128
        else:
            cmd = QIK_MOTOR_M0_REVERSE if reverse else QIK_MOTOR_M0_FORWARD, speed

        self.write(cmd)

    def setM1Speed(self, speed):
        reverse = False

        if (speed < 0):
            speed = -speed; # make speed a positive quantity
            reverse = True; # preserve the direction

        if (speed > 255):
            speed = 255

        if (speed > 127):
            # 8-bit mode: actual speed is (speed + 128)
            cmd = QIK_MOTOR_M1_REVERSE_8_BIT if reverse else QIK_MOTOR_M1_FORWARD_8_BIT, speed - 128
        else:
            cmd = QIK_MOTOR_M1_REVERSE if reverse else QIK_MOTOR_M1_FORWARD, speed

        self.write(cmd)

    def setSpeeds(self, m0Speed, m1Speed):
        self.setM0Speed(m0Speed)
        self.setM1Speed(m1Speed)



class PololuQik2s9v1(PololuQik):
    def __init__(self, port, resetPin):
        super().__init__(port, resetPin)

    def setM0Coast(self):
        self.write(QIK_2S9V1_MOTOR_M0_COAST)

    def setM1Coast(self):
        self.write(QIK_2S9V1_MOTOR_M1_COAST)

    def setCoasts(self):
        self.setM0Coast()
        self.setM1Coast()

class PololuQik2s15v9(PololuQik):
    def __init__(self, port, resetPin):
        super().__init__(port, resetPin)

    def setM0Brake(self, brake):
        if (brake > 127):
            brake = 127
        
        cmd = QIK_2S12V10_MOTOR_M0_BRAKE, brake
        self.write(cmd)

    def setM1Brake(self, brake):
        if (brake > 127):
            brake = 127
        
        cmd = QIK_2S12V10_MOTOR_M1_BRAKE, brake
        self.write(cmd)
    
    def setBrakes(self, m0Brake, m1Brake):
        self.setM0Brake(m0Brake)
        self.setM1Brake(m1Brake)

    def getM0Current(self):
        #self.listen()
        self.write(QIK_2S12V10_GET_MOTOR_M0_CURRENT)
        #while (self.available() < 1):
        #    pass
        return self.read()

    def getM1Current(self):
        #self.listen()
        self.write(QIK_2S12V10_GET_MOTOR_M1_CURRENT)
        #while (self.available() < 1):
        #    pass
        return self.read()

    def getM0CurrentMilliamps(self):
        return self.getM0Current() * 150

    def getM1CurrentMilliamps(self):
        return self.getM1Current() * 150

    def getM0Speed(self):
        #self.listen()
        self.write(QIK_2S12V10_GET_MOTOR_M0_SPEED)
        #while (self.available() < 1):
        #    pass
        return self.read()

    def getM1Speed(self):
        #self.listen()
        self.write(QIK_2S12V10_GET_MOTOR_M1_SPEED)
        #while (self.available() < 1):
        #    pass
        return self.read()

PololuQik2s12v10 = PololuQik2s15v9