# coding=utf-8
import hashlib
from src import app, socketio, network_config
from threading import Thread
from time import sleep
import requests
import multiprocessing
from utils.normalize import normalize_results
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required
from flask_socketio import send, emit
from core.ble_read_state import Ble_Read
from core.airdrop_leak import AirdropLeak

ble_read = None
airdrop_leak = None


@socketio.on_error()        
def error_handler(e):
    print(e)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

@socketio.on('device_received')
def device_status():
    global ble_read
    global airdrop_leak
    if(not ble_read):
        print(f"{network_config.w_iface}  {network_config.b_iface} {network_config.channel}")
        ble_read = Ble_Read(ble_iface=network_config.b_iface, w_iface=network_config.w_iface)

    if(not airdrop_leak):
        airdrop_leak = AirdropLeak(iface=network_config.w_iface, channel=network_config.channel)

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

@app.route('/change-channel', methods=['GET'])
def changeChannel():
    global airdrop_leak
    channel = request.args.get('channel', '6')
    airdrop_leak = AirdropLeak(iface=network_config.w_iface, channel=network_config.channel)
    thread = Thread(target=airdrop_leak.run, args=())
    thread.start()
    print("Restarting airdrop...")



