# -*- coding: utf-8 -*-
__author__ = 'hebin'

import requests
import json
from common.mylogging import mylogger
from common.config_read import get_xdotool_api

logger = mylogger()
header = {
        "Content-Type": "application/json;charset=UTF-8",
        }
url = get_xdotool_api()


class CommonControl(object):
    def __init__(self, ip, port=10810, username="root", password="Qq3j-sxNo.1"):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def set_key(self, key, delay=12):
        data = {
            "ip": self.ip,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "key": key,
            "delay": delay
        }
        data_str = json.dumps(data)
        logger.info("this url: %s" % url)
        logger.info("this post data: %s" % data_str)

        r = requests.post(url, data=data_str, headers=header)
        print r.text
        result = r.json()

        if result.get("success", None):
            logger.info("post request is ok, msg: %s" % result)
        else:
            raise Exception("post request is false, result: %s" % result)
