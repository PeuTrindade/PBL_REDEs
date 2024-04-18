import socket
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import json
import sys
sys.path.append('utils')
from auxFunctions import start_broker_server, connectedDevices, change_device_mode, change_device_temperature

app = Flask(__name__)
CORS(app)

@app.route('/devices', methods=['GET'])
def get_devices():
    return jsonify(connectedDevices), 200

@app.route('/change_mode/<ip_address>/<mode>', methods=['PATCH'])
def send_mode_command(ip_address, mode):
    try:
        if mode == 'on' or mode == 'off':
            change_device_mode(ip_address, mode)
        
            return jsonify({ "message": "Ok"}), 200
        else:
            return jsonify({ "message": "Envie um comando válido!"}), 400
    except e:
        return jsonify({ "message": "Falha ao enviar comando!"}), 500

@app.route('/change_temperature/<ip_address>/<temperature>', methods=['PATCH'])
def send_temperature_command(ip_address, temperature):
    try:
        if temperature and str(temperature).isdigit():
            change_device_temperature(ip_address, temperature)
        
            return jsonify({ "message": "Ok"}), 200
        else:
            return jsonify({ "message": "Envie um comando de temperatura válido!"}), 400
    except e:
        return jsonify({ "message": "Falha ao enviar comando!"}), 500

if __name__ == '__main__':
    # Inicia a thread para o servidor como broker
    broker_thread = threading.Thread(target=start_broker_server)
    broker_thread.start()
    
    # Inicia o servidor Flask
    app.run()