import os
import configparser


class Configuration:

    def __init__(self):
        self.config = configparser.RawConfigParser()
        self.config.read(os.path.dirname(os.path.abspath(__file__)) + '/config.ini')
        self.hosts = self.config.get('ssh', 'hosts').split(',')
        self.port = int(self.config.get('ssh', 'port'))
        self.login = self.config.get('ssh', 'login')
        self.password = self.config.get('ssh', 'password')
        self.log_path = self.config.get('ssh', 'log_path')
