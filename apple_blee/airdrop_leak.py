# Adapting script from https://github.com/hexway/apple_bleee
# Thanks to Dmitry Chastuhin @_chipik and https://hexway.io 
# Author: @lucferbux
from core.airdrop_leak import AirdropLeak
import argparse

def create_parser():
    help_desc = '''
    AirPods advertise spoofing PoC
    ---chipik
    '''
    parser = argparse.ArgumentParser(description=help_desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-n', '--name', default="evil-drop", help='Name of the interface')
    parser.add_argument('-i', '--iface', default='wlan0', help='Wireless inteface')
    parser.add_argument('-p', '--phone', default='34666666666', help='phone')
    parser.add_argument('-m', '--mail', default='example@gmail.com', help='mail')
    return parser.parse_args()

if __name__ == "__main__":
    args = create_parser()
    aidrop_leak = AirdropLeak(args=args)
    aidrop_leak.run()
