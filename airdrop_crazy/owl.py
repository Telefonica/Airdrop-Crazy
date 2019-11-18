from utils.ble_apple.wireless_interface import BadInterfaceException, ModeMonitorException, OwlException, check_wifi_config
from time import sleep

if __name__ == "__main__":
    check_wifi_config("wlx503eaaec4c39")
    try:
        while(True):
            sleep(5)
    except:
        print("Bye")