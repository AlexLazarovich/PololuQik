import RPi.GPIO as GPIO

class ResetPin:
    def __init__(self, pin_number, pin_numbering = GPIO.BCM, set_warning = False, inital_value = GPIO.LOW, active_value = GPIO.LOW):
        self._pin_number = pin_number
        self._active_value = active_value
        # GPIO setup
        GPIO.setmode(pin_numbering)  # use BCM pin numbering
        GPIO.setwarnings(set_warning)
        GPIO.setup(pin_number, GPIO.OUT, initial=inital_value)  # Set as output and initialize as LOW - aka turned off

    def turnOff(self):
        GPIO.output(self._pin_number, ~self._active_value)

    def turnOn(self):
        GPIO.output(self._pin_number, self._active_value)