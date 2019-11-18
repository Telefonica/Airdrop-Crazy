import utils.npyscreen as npyscreen
from utildata.apple_ble_states import phone_states, airpods_states, devices_models, ble_packets_types, dev_types, dev_sig
from threading import Thread, Timer
from prettytable import PrettyTable
import curses
import sys
import time
import subprocess

class App(npyscreen.StandardApp):

    def __init__(self, airdrop, utils):
        super().__init__()
        self.airdrop = airdrop
        self.utils = utils
        if(not utils.debug):
            self.titles = ['Mac', 'State', 'Device', 'Airdrop', 'OS', 'Rssi']
        else:
            self.titles = ['Mac', 'State', 'Device', 'Airdrop', 'OS', 'Header', 'Data', 'Rssi', 'Packet']

    """Main class attach a new app with the given form name
    
    Args:
        npyscreen (StandarApp): Standar NPyScreen Application
    """
    def onStart(self):
        self.addForm("MAIN", MainForm, name="Apple devices scanner (ctr+C to Quit)")


class MyGrid(npyscreen.GridColTitles):
    """Custom Grid class defining colors of the different labels
    
    Args:
        npyscreen (GridColTitles): Type of grid col
    """
    def custom_print_cell(self, actual_cell, cell_display_value):
        if 'Off' in cell_display_value or '<error>' in cell_display_value or 'iOS10' in cell_display_value or 'iOS11' in cell_display_value or 'iOS12' in cell_display_value:
            actual_cell.color = 'DANGER'
        elif 'Home screen' in cell_display_value or 'On' in cell_display_value or cell_display_value[0:3] in '\n'.join(dev_types) or 'macOS' in cell_display_value or 'X' in cell_display_value or 'Calling' in cell_display_value or cell_display_value in airpods_states.values() or 'WatchOS' in cell_display_value or 'Watch' in cell_display_value or 'iOS13' in cell_display_value or 'Connecting' in cell_display_value or 'WiFi screen' in cell_display_value or 'Homepod' in cell_display_value or 'iOS' in cell_display_value or 'Incoming' in cell_display_value or 'Outgoing' in cell_display_value: 
            actual_cell.color = 'GOOD'
        elif 'Lock screen' in cell_display_value or '-' in cell_display_value or 'iOS12' in cell_display_value:
            actual_cell.color = 'CONTROL'
        else:
            actual_cell.color = 'DEFAULT'


class OutputBox(npyscreen.BoxTitle):
    """Output Box Widget shown in airdrop mode
    
    Args:
        npyscreen (BoxTitle): Hybrid of Title widget and Multiline Widget, displays a box widget within the app
    """
    _contained_widget = npyscreen.MultiLineEdit



class MainForm(npyscreen.FormBaseNew):

    def create(self):
        """Creates the main form of the Npyscreen
        """
        titles = self.parentApp.titles
        new_handlers = {
            "^C": self.exit_func
        }
        self.add_handlers(new_handlers)
        y, x = self.useable_space()
        if self.parentApp.airdrop:
            self.gd = self.add(MyGrid, col_titles=titles, column_width=20, max_height=y // 2)
            self.OutputBox = self.add(OutputBox, editable=False)
        else:
            self.gd = self.add(MyGrid, col_titles=titles, column_width=20)
        self.gd.values = []
        self.gd.add_handlers({curses.ascii.NL: self.upd_cell})

    def while_waiting(self):
        self.gd.values = self.print_results()
        if self.parentApp.airdrop:
            self.OutputBox.value = self.print_wifi_devs()
            self.OutputBox.display()

    def exit_func(self, _input):
        """Exits the main app
        
        Args:
            _input (input): Input used to quit the func
        """
        self.parentApp.utils.disable_ble()
        # print("Bye")
        sys.exit(0)

    def get_dev_name(self, mac_addr):
        """Get device name name
        
        Args:
            mac_addr (bytes): Mac address of the device
        """
        dev_name = ''
        kill = lambda process: process.kill()
        cmd = ['gatttool', '-t', 'random', '--char-read', '--uuid=0x2a24', '-b', mac_addr]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        timer = Timer(3, kill, [proc])
        try:
            timer.start()
            dev_name, stderr = proc.communicate()
        finally:
            timer.cancel()
        if dev_name:
            d_n_hex = dev_name.split(b"value:")[1].replace(b" ", b"").replace(b"\n", b"")
            d_n_str = bytes.fromhex(d_n_hex.decode("utf-8")).decode('utf-8')
            return_value = devices_models[d_n_str]
        else:
            return_value = "<error>"
        self.parentApp.utils.init_bluez()
        if return_value:
            self.parentApp.utils.resolved_devs.append(mac_addr)
            # self.set_device_val_for_mac(mac_addr, return_value)

    def clear_zombies(self):
        """Clear all the zombies generated
        """
        cur_time = int(time.time())
        for device in list(self.parentApp.utils.phones):
            if cur_time - self.parentApp.utils.phones[device]['time'] > self.parentApp.utils.ttl:
                del self.parentApp.utils.phones[device]
                if self.parentApp.utils.resolved_macs.count(device):
                    self.parentApp.utils.resolved_macs.remove(device)
                if self.parentApp.utils.resolved_devs.count(device):
                    self.parentApp.utils.resolved_devs.remove(device)
                if self.parentApp.utils.victims.count(device):
                    self.parentApp.utils.victims.remove(device)


    def print_results(self):
        """Print the status of all the phones added
        
        Returns:
            [type]: [description]
        """
        self.clear_zombies()
        row = []
        if(not self.parentApp.utils.debug):
            for phone, value in self.parentApp.utils.phones.items():
                row.append([phone, value.get('state', "<unknown>"), value.get('device', "<unknown>"), value.get('airdrop', "<unknown>"), 
                value.get('os', "<unknown>"), value.get('rssi', "<unknown>")])
        else:
            for phone, value in self.parentApp.utils.phones.items():
                row.append([phone, value.get('state', "<unknown>"), value.get('device', "<unknown>"), value.get('airdrop', "<unknown>"), 
                value.get('os', "<unknown>"), value.get('header', "<unknown>"), value.get('data', "<unknown>"), value.get('rssi', "<unknown>"), (value.get('hash1', ""), value.get('hash2', ""))]) # debug

        return row

    def print_results2(self, data):
        """Print results of the airdrop utility
        
        Args:
            data (dict): Dictionary with the data
        
        Returns:
            [type]: [description]
        """
        x = PrettyTable()
        x.field_names = ["Phone", "Name", "Carrier", "Region", "Status", 'iMessage']
        for phone, value in data.items():
            x.add_row([value.get('phone', "<unknown>"), value.get('name', "<unknown>"), value.get('carrier', "<unknown>"), 
            value.get('region', "<unknown>"), value.get('status', "<unknown>"), value.get('iMessage', "<unknown>")])

        return x.get_string()


    def print_wifi_devs(self):
        results = self.parentApp.utils.get_airdrop_devices()
        return self.print_results3(results)

    def print_results3(self, devices):
        if not len(devices):
            return ''
        
        x = PrettyTable()
        x.field_names = ["Name", "Host", "OS", "Discoverable", 'Address']
        for dev in devices:
            x.add_row([dev.get('name', ''), dev.get('host', ''), dev.get('os', ''), dev.get('discoverable', ''), dev.get('address', '')])
        return x.get_string()

    # def check_exist(self, new_devices, actual_devices):
    #     ids = [dev.get('id') for dev in actual_devices]
    #     devices_filtered = [dev for dev in new_devices if dev.get('id' not in ids)]
    #     return devices_filtered

    # ------------ UTILS --------------------------
    def get_mac_val_from_cell(self):
        return self.gd.values[self.gd.edit_cell[0]][0]

    def get_state_val_from_cell(self):
        return self.gd.values[self.gd.edit_cell[0]][1]

    def get_device_val_from_cell(self):
        return self.gd.values[self.gd.edit_cell[0]][2]

    def get_wifi_val_from_cell(self):
        return self.gd.values[self.gd.edit_cell[0]][3]

    def get_os_val_from_cell(self):
        return self.gd.values[self.gd.edit_cell[0]][4]

    def get_phone_val_from_cell(self):
        return self.gd.values[self.gd.edit_cell[0]][5]

    def get_cell_name(self):
        titles = self.parentApp.titles
        return titles[self.gd.edit_cell[1]]

    def upd_cell(self, argument):
        cell = self.get_cell_name()
        if cell == 'Device':
            mac = self.get_mac_val_from_cell()
            thread2 = Thread(target=self.get_dev_name, args=(mac,))
            thread2.daemon = True
            thread2.start()