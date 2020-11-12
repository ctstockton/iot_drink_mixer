# This is an interface for interacting with the pumps
import time
import threading
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
except RuntimeError:
    print("""Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script.
        Couldn't creat create pump object.""")

class pump(object):
    """
    An interface for interacting with the pumps.
    """
    def __init__(self, pin_id, number, name='', ingr='', ingr_id=0):
        self.name = name
        self.number = number
        self.ingredient = ingr
        self.ingredient_id = ingr_id
        self.pin_id = pin_id
        #GPIO.setup(pin_id, GPIO.OUT, initial=GPIO.HIGH)

    def get_ingredient(self):
        return self.ingredient

    def set_ingredient(self, ingr):
        self.ingredient = ingr

    def get_ingredient_id(self):
        return self.ingredient_id

    def set_ingredient_id(self, ingr_id):
        self.ingredient_id = ingr_id

    def pump_fluid(self, time):
        GPIO.output(self.pin_id, GPIO.HIGH)
        time.sleep(time)
        GPIO.output(self.pin_id, GPIO.LOW)

    def run(self, time):
        self.pump_thread = threading.Thread(target=self.run, args=(time))
        self.pump_thread.start()

    def wait_for_finish(self):
        self.pump_thread.join()

    def is_alive(self):
        return self.pump_thread.is_alive()

    def get_number(self):
        return self.number

    
