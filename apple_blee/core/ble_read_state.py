# Adapting script from https://github.com/hexway/apple_bleee
# Thanks to Dmitry Chastuhin @_chipik and https://hexway.io 
# Author: @lucferbux
from utils.ble_apple.ble_utils import Ble_Apple_Utils
from utils.ble_apple.npyscreen_utils import App
from utils.ble_apple.wireless_interface import BadInterfaceException, ModeMonitorException, OwlException, check_wifi_config
from utildata.apple_ble_states import phone_states, airpods_states, devices_models, ble_packets_types
from utils.bluetooth_utils import (toggle_device)
from time import sleep
import sys
import json
import urllib3
import requests
import argparse
import multiprocessing
import time
import os
import signal
from os import path
from threading import Thread, Timer

class Ble_Read():

    def __init__(self, args=None, ttl=10, ble_iface=0, w_iface='wlan0', ssid=False, airdrop=False, debug=False):
        if(args):
            self.ttl = args.ttl
            self.ble_iface = args.ble_iface
            self.w_iface = args.w_iface
            self.ssid = args.ssid
            self.airdrop = args.airdrop
            self.debug = args.debug
        else:
            self.ttl = ttl
            self.ble_iface = ble_iface
            self.w_iface = w_iface
            self.ssid = ssid
            self.airdrop = airdrop
            self.debug = debug
        self.pr = None
        self.args = args
        self.ble_utils = None

    def service(self):
        toggle_device(self.ble_iface, True)
        self.ble_utils = Ble_Apple_Utils(self.ssid, self.airdrop, self.ttl, self.w_iface, self.ble_iface, self.debug)
        self.ble_utils.init_bluez()
        thread1 = Thread(target=self.ble_utils.do_sniff, args=(False,))
        thread1.daemon = True
        thread1.start()
        thread1.join()

    def get_info(self):
        return self.ble_utils.phones
        
    def cli(self):
        toggle_device(self.ble_iface, True)

        self.pr = multiprocessing.Process(target=self.read_state_cli, 
            args=(self.ssid, self.airdrop, self.ttl, self.w_iface, self.ble_iface, self.debug))
        try:
            self.pr.start()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.pr.terminate()
            print(f"Killing {self.pr.pid}")
            os.kill(self.pr.pid, signal.SIGTERM)

    def read_state_cli(self, ssid, airdrop, ttl, iwdev, dev_id, debug):
        """Read the state of the nearby Apple ble devices
        
        Args:
            ssid (Bool): Check to get ssid to phone results
            airdrop (Bool): Check the airdrop to get the phone hash
            ttl (int): Time to live to refresh
            iwdev (str): Wifi interface
            dev_id (int): Bluetooth interface
        """
        ble_utils = Ble_Apple_Utils(ssid, airdrop, ttl, iwdev, dev_id, debug)
        if airdrop:
            try:
                print("Configuring owl interface...")
                check_wifi_config(iwdev)
                sleep(4) # time to wake up owl process
            except ModeMonitorException:
                print("Error, mode monitor not suported in the given interface, press ctr+c to continue")
                return
            except BadInterfaceException:
                print("Error, inteface not found, press ctr+c to continue")
                return
            except OwlException:
                print("Error, there was a problem setting up owl, press ctr+c to continue, if not insalled --> https://github.com/seemoo-lab/owl.git")
                return
            except Exception as e:
                print(f"Error, something went wrong configuring the interface, press ctr+c to continue --> {e}")
                return

        if ssid:
            thread_ssid = Thread(target=ble_utils.get_ssids, args=())
            thread_ssid.daemon = True
            thread_ssid.start()
            thread2 = Thread(target=ble_utils.start_listetninig, args=())
            thread2.daemon = True
            thread2.start()

            thread3 = Thread(target=ble_utils.adv_airdrop, args=())
            thread3.daemon = True
            thread3.start()

        ble_utils.init_bluez()
        thread1 = Thread(target=ble_utils.do_sniff, args=(False,))
        thread1.daemon = True
        thread1.start()
        MyApp = App(airdrop, ble_utils)
        MyApp.run()
        thread1.join()

    
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
    return parser.parse_args()

if __name__ == "__main__":
    args = create_parser()
    airpods = Ble_Read(args)
    airpods.read()







