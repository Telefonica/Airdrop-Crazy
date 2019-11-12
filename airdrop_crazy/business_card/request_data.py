import re
from os import path
from importlib import import_module
from os import scandir, sep
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from timeit import timeit
from .api_services.everyoneapi import EveryoneApi
from .api_services.mobileconnect import MobileConnect

class RequestData():

    def __init__(self, phone=''):
        """Get information about the phone with the service everyone api
        (Due to private access we have drop the support of other services)
        
        Args:
            phone (str, optional): Phone number to get info. Defaults to ''.
        """
        self.phone = phone
        self.name = ''
        self.carrier = ''
        self.gender = ''
        self.country = ''
        self.response = {}

    def get_info(self):
        """Check info of Everyoneapi. Previously had more services
        
        Returns:
            {str:any}: Dictionary with the properties
        """
        everyone = EveryoneApi(phone=self.phone)
        carrier_everyone, name, gender = everyone.request_data()
        mobileconnect = MobileConnect(phone=self.phone)
        carrier_mobileconnect, country, currency = mobileconnect.request_data()
        self.name = name
        self.gender = gender
        self.carrier = carrier_everyone if carrier_everyone else carrier_mobileconnect
        self.country = country
        return {
            "name" : self.name,
            "number" : self.phone,
            "carrier" : self.carrier,
            "country" : self.country,
            "gender" : self.gender
        }
