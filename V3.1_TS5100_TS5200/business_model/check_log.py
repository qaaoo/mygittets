# -*-coding: utf-8 -*-
__author__ = "hebin"

import json
import re
from ssh_client import ssh_client
from common.mylogging import mylogger
from common_terminal_control import CommonControl

logger = mylogger()


def check_log(control, client_id, check_option):
    ip = control.ip
    port = control.port
    username = control.username
    password = control.password
    client = ssh_client(ip, port, username, password)
    reponse_log = client.exec_cmd(r"egrep '\[web-Receive-request\]\ *id=\ *\d*.*result.*onChangeConfControlStatus' /var/log/elink/elink.log|tail -1")
    logger.info("--- elink log: %s ---" % reponse_log)
    if not reponse_log:
        return False
    request_id = re.search(r'id=\s\d+', reponse_log).group()
    request_time = re.search(r'\d+:\d+:\d+', reponse_log).group()
    log_json = json.loads(re.search(r'\{.*\}', reponse_log).group())
    msg = log_json.get("msg", None)
    if msg != 'ok':
        return False
    for member in log_json['result']['params']['members']:
        if member['clientID'] != client_id:
            continue
        check_status = member[check_option]

    id_result = client.exec_cmd(r"egrep '\[web-response-post\].*%s' /var/log/elink/elink.log|tail -1" % request_id)
    logger.info('--- elink log: %s ---' % id_result)
    if re.search(r"\"message\":\"ok\"", id_result):
        return 'ok', check_status, request_time
    return False


if __name__ == "__main__":
    control = CommonControl("10.35.32.63")
    print check_log(control, "20001018", "isSpeakerOpen")
