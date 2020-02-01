# Adapting script from https://github.com/gstaff/flask-ngrok thanks to @gstaff

from subprocess import Popen, PIPE, STDOUT, DEVNULL
from time import sleep
from atexit import register
import json
import qrcode
import os
import zipfile
import requests
from pathlib import Path
from threading import Timer


def create_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.show()

def detect_ngrok():
    r = Popen(["curl", "http://localhost:4040/api/tunnels"], stdout=PIPE, stderr=PIPE)
    try:
        output_raw = r.stdout.read().decode()
        output = json.loads(output_raw)
        url = output["tunnels"][0]["public_url"]
        create_qr(url)
    except Exception as e:
        print("Ngrok not configured, trying to start")
        thread = Timer(1, start_ngrok, args=(5000,))
        thread.setDaemon(True)
        thread.start()
        
def _run_ngrok(port):
    executable = str(Path("./ngrok", "ngrok"))
    ngrok = Popen([executable, 'http', str(port)], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sleep(1)
    r = Popen(["curl", "http://localhost:4040/api/tunnels"], stdout=PIPE, stderr=PIPE)
    try:
        output_raw = r.stdout.read().decode()
        output = json.loads(output_raw)
        url = output["tunnels"][0]["public_url"]
        return url
    except:
        print("Error configuring Ngrok")
        raise


def start_ngrok(port):
    ngrok_address = _run_ngrok(port)
    create_qr(ngrok_address)





