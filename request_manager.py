from pump_manager import pump_manager
from queue import Queue
from time import sleep
import sqlite3

class request_manager(object):
    """
    This class takes care of recieving a recipe and gives the instructions to the pump manager.
    """
    def __init__(self, q):
        # prepare reference to the recipe queue
        self.request_queue = q
        self.pm = pump_manager()

        # set up database connection
        self.conn = sqlite3.connect('ingredient.db')
        self.c = self.conn.cursor()

    def run(self):
        while(True):
            if(~self.request_queue.empty()):
                # get request
                current_request = self.request_queue.get()
                # identify request
                if(current_request['request-type'] == 'recipe'):
                    print('From request_manager:')
                    print(current_request['amount'])
                    print(current_request['unit'])
                    print(current_request['recipe'])
                    print(current_request['ingredients'])

                    # get recipe id by using recipe name
                    self.c.execute('SELECT id FROM recipes WHERE name = ?', (current_request['recipe'],))
                    r_id = self.c.fetchall()[0][0]
                    print(r_id)

                    # now get ingredient ids that are involved and their amounts
                    self.c.execute('SELECT id_ingredient,amount FROM join_recipes_to_ingredients WHERE id_recipe = ?',(int(r_id),))
                    resluts = self.c.fetchall()
                    i_id = [int(row[0]) for row in resluts]
                    amounts = [float(row[1]) for row in resluts]
                    print('i_id: {}'.format(i_id))
                    print('amnt: {}'.format(amounts))
                    recipe = {
                        'ingredients-ids': i_id,
                        'amounts': amounts
                    }

                    # finally send to pump manager
                    self.pm.make(recipe, current_request['amount'], current_request['unit'])
                elif(current_request['request-type'] == 'prime'):
                    pass
                elif(current_request['request-type'] == 'clean'):
                    pass
                elif(current_request['request-type'] == 'assign'):
                    pass
            else:
                sleep(0.5)
