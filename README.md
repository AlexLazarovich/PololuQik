# PololuQik
PololuQik library for pololu qik motor controllers.
The library was built for RaspberryPi, but isn't dependent of it.

## Requirements
### RPi.GPIO
For RaspberryPi developers, only ResetPin.py is dependent of this, but PololuQik.py expects it's ResetPin to have turnOff/turnOn functions(See ResetPin.py for example).

    pip install RPi.GPIO


### pyserial
For pyserial API used in PololuQik.py

    pip install pyserial


## multi_controller_init.py
Shows how to init multiple controllers on same bus, **Should only be executed Once!**
