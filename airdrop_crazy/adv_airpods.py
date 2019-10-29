# Adapting script from https://github.com/hexway/apple_bleee
# Thanks to Dmitry Chastuhin @_chipik and https://hexway.io 
# Author: @lucferbux
from core.adv_airpods import AdvAirpods
import argparse

def create_parser():
    help_desc = '''
    AirPods advertise spoofing PoC
    ---chipik
    '''
    parser = argparse.ArgumentParser(description=help_desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--interval', default=200, type=int, help='Advertising interval')
    parser.add_argument('-r', '--random', action='store_true', help='Send random charge values')
    parser.add_argument('-b', '--ble_iface', default=0, type=int, help='Bluetooth inteface')
    return parser.parse_args()

if __name__ == "__main__":
    args = create_parser()
    airpods = AdvAirpods(args=args)
    airpods.advertisment()

