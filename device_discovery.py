#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 14:59:49 2023

@author: ghak
"""

import threading
import time
import socket
import traceback
import sys

class DeviceDiscovery(threading.Thread):
    # 30 seconds for search_interval
    

    def __init__(self, search_interval=5, interface='eth0'):
        self.SEARCH_INTERVAL = search_interval
        self.SSDP_ADDR = '239.255.255.250'
        self.SSDP_PORT = 1900
        self.SSDP_MX = 1;
        self.SSDP_ST = "urn:schemas-sony-com:service:ScalarWebAPI:1";
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, interface.encode('utf-8'))
        self.sock.settimeout(5)
        threading.Thread.__init__(self)
        self.interrupted = False
        
        self.connected = False
        self.host = ''
        self.port = ''
        self.res = ''
        
        
    def run(self):
        print("running")
        try:
            while True:
                self.search()
                if self.connected:
                    return (self.host, self.port, self.res)
                for x in range(self.SEARCH_INTERVAL):
                    time.sleep(1)
                    if self.interrupted:
                        self.sock.close()
                        return
        except Exception as e:
            self.sock.close()
            print('Error in upnp client keep search %s', e)
    
    def stop(self):
        self.interrupted = True
        print("upnp client stop")
    
    def search(self):
        '''
        broadcast SSDP DISCOVER message to LAN network
        filter our protocal and add to network
        '''
        try:
            SSDP_DISCOVER = "M-SEARCH * HTTP/1.1\r\n" + \
                    		"HOST: %s:%d\r\n" % (self.SSDP_ADDR, self.SSDP_PORT) + \
                            "MAN: \"ssdp:discover\"\r\n" + \
                            "MX: %d\r\n" % (self.SSDP_MX, ) + \
                            "ST: %s\r\n" % (self.SSDP_ST, ) + "\r\n";
            
            print("sending message ...")
            self.sock.sendto(SSDP_DISCOVER.encode('utf-8'), (self.SSDP_ADDR, self.SSDP_PORT))
            while not(self.connected):
                print("waiting for data....")
                data, (self.host, self.port) = self.sock.recvfrom(1024)
                data = data.decode('utf-8')
                self.res = self.parse(data)
                self.connected = True
        except :
            traceback.print_exc()
         
    def get_connection_informations(self):
        if self.connected == True:
            return (self.host, self.port, self.res)
        else:
            return (False, False, False)
         
    def parse(self, data):
        lines = data.split('\r\n')
        res = {}
        if (lines[0] != 'HTTP/1.1 200 OK'):
            print("Warning : Header different of expected %s", lines[0])
        for line in lines[1:]:
            if line:
                try:
                    key, val = line.split(': ', 1)
                    res[key.lower()] = val
                except:
                    print("Warning : Cannot parse SSDP response for this line: %s", line)
                    pass
        if res:
            return res
        else:
            print("Error : No headers received")
            sys.exit(1)