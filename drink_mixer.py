# This is the drink mixer object
from queue import Queue
from threading import Thread
from request_manager import request_manager
from webhook_service import webhook_service

class drink_mixer(object):
    """
    This is the drink mixer object, managing local and remote requests.
    """
    def __init__(self):
        self.q = Queue()
        self.webhook_service = webhook_service(self.q)
        self.webhook_service_thread = Thread(target=self.webhook_service.run)
        #self.GUI_service = Thread()#target=, args=(self.q, ))

        self.request_manager = request_manager(self.q)

    def run(self):
        # start threads
        self.webhook_service_thread.start()
        #self.GUI_service.start()

        # start manager of the main thread
        self.request_manager.run()

if __name__ == "__main__":
    drinkMixer = drink_mixer()
    drinkMixer.run()
