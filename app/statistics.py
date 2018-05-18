#!/usr/bin/python3
import argparse
import re
from ssh import Ssh
from db import Db
from config import Configuration
from datetime import datetime, timedelta


class Init:

    def __init__(self):
        args = self.input()
        self.dates = self.add_hour(args)

    def input(self):
        arg = argparse.ArgumentParser(description='11', prog='parser')
        arg.add_argument('--from', type=str, default=None, required=True, help='from date')
        arg.add_argument('--to', type=str, default=None, required=True, help='to date')
        args = vars(arg.parse_args())
        return args

    def add_hour(self, args):
        try:
            date_from = datetime.strptime(args['from'], '%Y-%m-%d %H:%M:%S')
            date_to = datetime.strptime(args['to'], '%Y-%m-%d %H:%M:%S')
            date_from += timedelta(hours=1)
            date_to += timedelta(hours=1)
            ret = [date_from, date_to]
            return ret
        except ValueError as e:
            print(e)


class Parser:

    def __init__(self):
        self.config = Configuration()
        self.launch = Init()
        date_from = self.launch.dates[0]
        date_to = self.launch.dates[1]
        self.db = Db()
        for host in self.config.hosts:
            self.ssh = Ssh(host, 22, self.config.login, self.config.password)
            logs = self.find_logs(date_from, date_to)
            for log in logs:
                strings = self.find_strings(log)
                batch_counter = 0
                batch = []
                for string in strings:
                    parsed = self.parse_row(string)
                    if re.match(r'(\d{4})-(\d{2})-(\d{2})', parsed[0]):
                        batch.append(parsed)
                        batch_counter += 1
                    if batch_counter >= 100:
                        self.db.insert(batch)
                        batch = []
                        batch_counter = 0

    def find_logs(self, date_from, date_to):
        try:
            cmd = "find {0}/ -maxdepth 1  -name 'server.log.*' -newermt '{1}' " \
                  "! -newermt '{2}' | sort".format(self.config.log_path, date_from, date_to)
            logs = self.ssh.remote_cmd(cmd)
            return logs
        except ValueError as e:
            print(e)

    def find_strings(self, log):
        try:
            cmd = "zgrep -a 'INFO' {0} | zgrep -a '\[statistics\]' ".format(log)
            cmd += "| awk '{ print $1\" \"$2\";\"$7}'"
            strings = self.ssh.remote_cmd(cmd)
            return strings
        except ValueError as e:
            print(e)

    def parse_row(self, row):
        date = row.split(';')[0].split(',')[0]
        method = row.split(';')[1]
        result = [date, method]
        return result

parser = Parser()