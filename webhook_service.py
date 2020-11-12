from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher

class webhook_service(object):
    """
    An intergace for managing the webhook service.
    """
    def __init__(self, q):
        self.q = q

    def run(self):
        self.app = Flask(__name__)
        @self.app.route('/', methods=['POST'])
        def index():
            data = request.get_json(silent=True)
            #print(data)
            #print(data['responseId'])
            #print(data['queryResult']['parameters']['unit-weight']['amount'])
            #print(data['queryResult']['parameters']['unit-weight']['unit'])
            #print(data['queryResult']['parameters']['recipe'])
            #print(data['queryResult']['parameters']['ingredient'])
            amount = data['queryResult']['parameters']['unit-weight']['amount']
            unit = data['queryResult']['parameters']['unit-weight']['unit']
            recipe = data['queryResult']['parameters']['recipe']
            ingredients = data['queryResult']['parameters']['ingredient']
            request_to_queue = {
                'request-type': 'recipe',
                'amount': amount,
                'unit': unit,
                'recipe': recipe,
                'ingredients': ingredients
            }
            self.q.put(request_to_queue)
            reply = {
                "fulfillmentText": data['queryResult']['fulfillmentText']
            }
            return jsonify(reply)
        self.app.run()


if __name__ == "__main__":
    from queue import Queue
    q = Queue()
    whs = webhook_service(q)
    whs.run()
