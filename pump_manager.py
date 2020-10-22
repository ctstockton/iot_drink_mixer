import pump

class pump_manager(object):
    """
    This class takes the normalized recipe. It then checks the pumps' ingredients. If a recipe can be made, it will turn the pumps on for the respective time.
    """
    def __init__(self, num_of_pumps):
        self.num_of_pumps = num_of_pumps

        # Create queue for recipes
        self.recipes = []
        
        self.pumps = []
        self.pump_pins = []

        # Create list of pumps with their names on startup
        pump_num = 1
        for pin in self.pump_pins:
            self.pumps.append(pump(pin, "Pump "+str(pump_num)))
            pump_num++
    
    def make(self, recipe, amount):
        pass
