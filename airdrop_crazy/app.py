from src import app, socketio, network_config
from utils.setup_flask import detect_ngrok
from utils.ble_apple.wireless_interface import check_wifi_config
import argparse


def create_parser():
    help_desc = '''
    Airdrop Crazy server
    '''
    parser = argparse.ArgumentParser(description=help_desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-w', '--wiface', default='wlan0', help='Wireless inteface')
    parser.add_argument('-b', '--biface', default=0, help='HCI Interface')
    parser.add_argument('-c', '--channel', default='6', help='Channel of OWL [6, 44, 149]')
    return parser.parse_args()





if __name__ == '__main__':
    try:
        args = create_parser()
        print("creating app")
        network_config.w_iface = args.wiface
        network_config.b_iface = args.biface
        network_config.channel = args.channel
        check_wifi_config(args.wiface, args.channel)
        detect_ngrok()
        socketio.run(app)
    except Exception as e:
        print("Error setting the server")
