# -*- coding:utf-8 -*-

import paramiko
import logging


class ssh_client(object):
    def __init__(self, ip, port=10810, username="root", password="Qq3j-sxNo.1"):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = int(port)
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        try:
            self.client.connect(self.ip, self.port, self.username, self.password, timeout=100)
        except Exception as e:
            raise e

    def exec_cmd(self, cmd):
        self.connect()
        stdin, stdout, stderr = self.client.exec_command(cmd, timeout=20)
        error = stderr.read()
        if error:
            self.close()
            raise Exception("cmd: %s exec failed, error is %s" % (cmd, error))
        result = stdout.read()
        logging.debug("cmd: %s success, message is: %s" % (cmd, result))
        self.close()
        return result

    def close(self):
        self.client.close()


if __name__ == "__main__":
    client = ssh_client("10.35.32.63", port=10810)
    r = client.exec_cmd("grep '\[web-Receive-request\].*onChangeConfControlStatus' /var/log/elink/elink.log|tail -1")
    print r
