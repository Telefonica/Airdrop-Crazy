# Adapting script from https://github.com/hexway/apple_bleee
# Thanks to Dmitry Chastuhin @_chipik and https://hexway.io 
# Author: @lucferbux
from core.adv_wifi import AdvWifi
import argparse

def create_parser():
    help_desc = '''
    AirPods advertise spoofing PoC
    ---chipik
    '''
    parser = argparse.ArgumentParser(description=help_desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--interval', default=200, type=int, help='Advertising interval')
    parser.add_argument('-b', '--ble_iface', default=0, type=int, help='Bluetooth inteface')
    parser.add_argument('-p', '--phone', default='none', help='Phone number (example: 39217XXX514')
    parser.add_argument('-e', '--email', default='none', help='Email address (example: test@test.com)')
    parser.add_argument('-a', '--appleid', default='none', help='AppleID')
    parser.add_argument('-s', '--ssid', required=True, help='WiFi SSID (example: test)')
    return parser.parse_args()

if __name__ == "__main__":
    args = create_parser()
    wifi = AdvWifi(args=args)
    wifi.advertisment()