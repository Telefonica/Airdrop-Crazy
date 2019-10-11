# coding=utf-8
import hashlib
from src import app
from threading import Thread
import time
import requests
import multiprocessing
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required

# # import core
from core.ble_read_state import Ble_Read

ble_read = Ble_Read()
   
@app.route('/ble-config', methods=['GET'])
def start_ble():    
    thread = Thread(target=ble_read.service, args=())
    thread.start()

    return jsonify(
        {"ok": "ok"}
    )

@app.route('/device-status', methods=['GET'])
def device_status():
    devices = ble_read.get_info()
    return jsonify(
        {"devices": devices}
    )
    