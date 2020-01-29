from subprocess import Popen, PIPE
import os
import signal
from time import sleep

class BadInterfaceException(Exception):
    pass

class ModeMonitorException(Exception):
    pass

class OwlException(Exception):
    pass

def check_wifi_config(iwdev, channel, verbose=False):
    """Restart the interface, change it to monitor mode and enable owl for airdrop
    
    Args:
        iwdev (str): Interface name
    
    Raises:
        Exception: Bad Interface Exception
        Exception: Mode monitor Exception
    """
    result = Popen(["iwconfig", iwdev], stdout=PIPE, stderr=PIPE)
    if(result.stderr.read()):
        # exception bad interface
        raise BadInterfaceException
    r = Popen(["airmon-ng", "check", "kill"], stdout=PIPE, stderr=PIPE)

    sleep(1)
    owl_result = check_owl_process()

    if(owl_result):
        process_id = owl_result.lstrip(' ').split(" ")[0]
        os.kill(int(process_id), signal.SIGTERM)

    # 6, 44, 149
    if(verbose):
        result = Popen(["owl", "-i", iwdev, "-c", channel, "-v"])
    else:
        result = Popen(["owl", "-i", iwdev, "-D", "-c", channel], stdout=PIPE, stderr=PIPE)
    if(result.stderr.read()):
        print("Error")
        raise OwlException



def check_owl_process():
    ps = Popen(["ps", "-A"], stdout=PIPE)
    grep = Popen(["grep", "owl"], stdin=ps.stdout, stdout=PIPE)
    return grep.stdout.read().decode()