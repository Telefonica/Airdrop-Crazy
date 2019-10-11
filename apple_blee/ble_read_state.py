# Adapting script from https://github.com/hexway/apple_bleee
# Thanks to Dmitry Chastuhin @_chipik and https://hexway.io 
# Author: @lucferbux
from core.ble_read_state import Ble_Read
import argparse
  
def create_parser():
    help_desc = '''
    AirPods advertise spoofing PoC
    ---chipik
    '''
    parser = argparse.ArgumentParser(description=help_desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t', '--ttl', default=10, type=int, help='Time To Live')
    parser.add_argument('-b', '--ble_iface', default=0, type=int, help='Bluetooth inteface')
    parser.add_argument('-w', '--w_iface', default='wlan0', help='Wireless Interface')
    parser.add_argument('-s', '--ssid', action='store_true', help='Get SSID from request')
    parser.add_argument('-a', '--airdrop', action='store_true', help='Get info from AWDL airdrop')
    parser.add_argument('-d', '--debug', action='store_true', help='Debug Mode')
    return parser.parse_args()

if __name__ == "__main__":
    args = create_parser()
    airpods = Ble_Read(args=args)
    #airpods.cli()
    airpods.service()







