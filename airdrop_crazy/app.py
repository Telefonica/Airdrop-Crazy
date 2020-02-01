from src import application, socketio, IFACE, CHANNEL
from utils.setup_flask import detect_ngrok
from utils.ble_apple.wireless_interface import check_wifi_config


if __name__ == '__main__':
    try:
        check_wifi_config(IFACE, CHANNEL)
        detect_ngrok()
        socketio.run(application)
    except Exception as e:
        print("Error setting the server, might be ngrok or setting up card")
