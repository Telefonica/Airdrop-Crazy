# coding=utf-8
import hashlib
from src import app, socketio
from threading import Thread
from time import sleep
import requests
import multiprocessing
from .utils import normalize_results
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required
from flask_socketio import send, emit
from core.ble_read_state import Ble_Read


ble_read = Ble_Read()

@socketio.on('connect')
def test_connect():
    print("user connected")

@socketio.on_error()        
def error_handler(e):
    print(e)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

@socketio.on('device_received')
def device_status():
    if(not ble_read.scanning):
        thread = Thread(target=ble_read.service, args=())
        thread.start()
        print("inicializamos...")
        socketio.sleep(1)

    while True:
        devices = ble_read.get_info()
        devices_parsed = normalize_results(devices)
        emit('when pressed',  devices_parsed)
        socketio.sleep(0.5)



