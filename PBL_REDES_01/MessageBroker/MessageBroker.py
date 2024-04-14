import socket
import threading
from flask import Flask, jsonify, request
import pickle
import json
import sys
sys.path.append('utils')
from auxFunctions import start_broker_server

app = Flask(__name__)

@app.route('/devices', methods=['GET'])
def get_devices():
    try:
        with open('database/connectedDevices.pickle', 'rb') as dic:
            connectedDevices = pickle.load(dic)
    except (FileNotFoundError, EOFError):
        connectedDevices = {}
    
    return jsonify(connectedDevices)


if __name__ == '__main__':
    # Inicia a thread para o servidor como broker
    broker_thread = threading.Thread(target=start_broker_server)
    broker_thread.start()
    
    # Inicia o servidor Flask
    app.run(debug=True)