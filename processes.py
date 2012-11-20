# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 23:33:38 2012

@author: panter
"""

import os
import fileinput

PATH = "/proc/"


def get_cmd(process_id):
    """get_cmd"""
    try:
        cmd_file = fileinput.input(PATH + process_id + "/cmdline")
        result = cmd_file.readline().replace('\x00', '')

    except IOError as error:
        result = str()
        print(error)

    finally:
        cmd_file.close()
    return result


def get_status(process_id):
    """get_status"""
    result = str()
    try:
        status_file = fileinput.input(PATH + process_id + "/status")
        for status_line in status_file:
            if status_line.startswith("State:"):
                result = status_line.replace("State:\t", '')
                break
    except IOError as error:
        print(error)

    finally:
        status_file.close()
    return result


def get_processes_list():
    """get_processes_list"""
    result = []

    for process_id in os.listdir(PATH):
        if process_id.isdigit():
            cmd = get_cmd(process_id)
            if len(cmd) > 0:
                status = get_status(process_id)
                if len(status) > 0:
                    result.append(" ".join(status.split()) + " " + cmd)
    return result