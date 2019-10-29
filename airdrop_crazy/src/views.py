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
from core.airdrop_leak import AirdropLeak


ble_read = Ble_Read()
airdrop_leak = AirdropLeak(iface="") # Change the iface

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
        print("Starting ble...")
        socketio.sleep(1)

    if(not airdrop_leak.scanning):
        thread = Thread(target=airdrop_leak.run, args=())
        thread.start()
        print("Starting airdrop...")

    while True:
        devices = ble_read.get_info()
        people = airdrop_leak.get_people()
        devices_parsed = normalize_results(devices, "mac")
        people_parsed = normalize_results(people, "hash")
        emit('device_detected',  {"devices": devices_parsed, "people": people_parsed})
        socketio.sleep(0.5)



