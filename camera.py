# -*- coding: utf-8 -*-
import sys
import re
import requests
from urllib.request import urlopen
import device_discovery as dd

class Camera:
    def __init__(self, search_interval=5, interface='eth0'):
        a6000 = dd.DeviceDiscovery(interface='wlp4s0f0')
        self.host, self.port, self.headers = a6000.run()
        if self.host==False:
            print("Error: Can't connect to device")
            sys.exit(1)
        self.services = self.xml_parser(self.headers['location'])
        
    def start_remote_mode(self):
        print("Connecting to camera...")
        payload = {"version": "1.0", "id": 1, "method": "startRecMode", "params": []}
        r = requests.post(self.services['camera']+'/camera/', json=payload)
        if r.status_code != 200:
            print("Could not connect to camera: " + str(r.status_code))
            exit()
        print("Response: " + str(r.json()))
    
    def getSupportedLiveViewSize(self):
        print("Requesting supported device resolution ...")
        payload = {"version": "1.0", "id": 1, "method": "getSupportedLiveviewSize", "params": []}
        r = requests.post(self.services['camera']+'/camera/', json=payload)
        response = r.json()
        print("Response: " + str(response))
    
    def startLiveView(self, size):
        #Request preview stream
        print("Requesting stream...")
        payload = {"version": "1.0", "id": 1, "method": "startLiveviewWithSize", "params": [size]}
        r = requests.post(self.services['camera']+'/camera/', json=payload)
        response = r.json()
        url = response["result"][0]
        return url
    
    def xml_parser(self, location_xml):
        """
        Parse the XML device definition file.
        """
        xml_data = urlopen(location_xml).read()
        dd_regex = ('<av:X_ScalarWebAPI_Service>'
            '\s*'
            '<av:X_ScalarWebAPI_ServiceType>'
            '(.+?)'
            '</av:X_ScalarWebAPI_ServiceType>'
            '\s*'
            '<av:X_ScalarWebAPI_ActionList_URL>'
            '(.+?)'                             
            '</av:X_ScalarWebAPI_ActionList_URL>'
            '\s*'
            '<av:X_ScalarWebAPI_AccessType\s*/>' 
            '\s*'
            '</av:X_ScalarWebAPI_Service>')

        xml_data = xml_data.decode('utf8')
        services = {}
        for m in re.findall(dd_regex, xml_data):
            service_name = m[0]
            endpoint = m[1]
            services[service_name] = endpoint
        return services
