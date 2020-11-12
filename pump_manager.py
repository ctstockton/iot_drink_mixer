from pump import pump

class pump_manager(object):
    """
    This class takes the normalized recipe. It then checks the pumps' ingredients. If a recipe can be made, it will turn the pumps on for the respective time.
    """
    def __init__(self):
        
        # Set up pump pins list
        self.pumps = []
        self.pump_pins = [7,13,15,18,22,38]

        # Create list of pumps with their names on startup
        pump_num = 1
        for pin in self.pump_pins:
            self.pumps.append(pump(pin, pump_num, "Pump "+str(pump_num)))
            pump_num += 1
        
        # Add the time to ounce relationship
        # This is assumed to remain constant for all pumps and all liquids
        self.ounce_to_time = 20.94

        # for testing purposes, assign pumps here
        self.pumps[0].set_ingredient_id(4)
        self.pumps[0].set_ingredient('Tequila')
        self.pumps[1].set_ingredient_id(498)
        self.pumps[1].set_ingredient('Triple Sec')
        self.pumps[2].set_ingredient_id(312)
        self.pumps[2].set_ingredient('Lime')
    
    def make(self, recipe, amount, units):
        # cycle through ingredients a check if they are attached
        list_of_pumps_ids = self.check_pumps_for_all_ingr(
            recipe['ingredients-ids'])
        
        # compute scaler for recipe
        ratio = sum(recipe['amounts'])
        scaler = ratio/amount

        # now make the drink
        # turn on the pumps for their respective time
        print('Turning on pumps:')
        for i in range(len(list_of_pumps_ids)):
            self.pumps[list_of_pumps_ids[i]].run(scaler*recipe['amounts'][i]*self.ounce_to_time)
            print(str(scaler*recipe['amounts'][i]*self.ounce_to_time)+' s')
        print('From pump_manager:')
        print('Recipe is in the making.')
        for i in range(len(list_of_pumps_ids)):
            self.pumps[list_of_pumps_ids[i]].wait_for_finish()
        print('Finished.')

    def prime_pump(self, pump_num):
        self.pumps[pump_num].run(2)

    def assign_pump_ingr(self, pump_num, ingr, ingr_id):
        self.pumps[pump_num].set_ingredient(ingr)
        self.pumps[pump_num].set_ingredient_id(ingr_id)

    def clean_pump(self, pump_num):
        self.pumps[pump_num].run(10)

    def check_pumps_for_all_ingr(self, ingr_ids):
        hasAllIngr = []
        for i in ingr_ids:
            for p in self.pumps:
                if(p.get_ingredient_id() == i):
                    hasAllIngr.append(p.get_number())
        return hasAllIngr
        
