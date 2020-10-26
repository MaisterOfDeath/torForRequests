__author__ = 'Greatest'

import time
import urllib3
from stem import Signal
from stem.control import Controller


class ConnectionManager:
    def __init__(self):
        self.new_ip = "0.0.0.0"
        self.old_ip = "0.0.0.0"
        self.new_identity()

    def _get_connection(self):
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password='Hellchell1')
            controller.signal(Signal.NEWNYM)
            controller.close()

    def request(self, url):
        request = urllib3.ProxyManager('http://127.0.0.1:8118').request('GET', url)
        return request

    def new_identity(self):
        # First Connection
        if self.new_ip == "0.0.0.0":
            self._get_connection()
            self.new_ip = self.request('http://icanhazip.com').data.decode('utf-8')
            # print(self.new_ip.data.decode('utf-8'))
        else:
            self.old_ip = self.new_ip
            self._get_connection()
            self.new_ip = self.request('http://icanhazip.com').data.decode('utf-8')

        while self.old_ip == self.new_ip:
            time.sleep(5)
            print("Waiting to obtain new IP: %s Seconds" % 10)
            self.new_ip = self.request('http://icanhazip.com').data.decode('utf-8')
        print(self.new_ip, end='')

