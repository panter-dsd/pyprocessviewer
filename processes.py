# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 23:33:38 2012

@author: panter
"""

import io
import os
import fileinput

PATH="/proc/"


def get_cmd(process_id):
    cmd_file = fileinput.input(PATH + process_id + "/cmdline")
    result = cmd_file.readline().replace('\x00', '')
    cmd_file.close()
    return result
    
def get_status(process_id):
    status_file = fileinput.input(PATH + process_id + "/status")
    for status_line in status_file:
        if status_line.startswith("State:"):
            status_file.close()
            return status_line.replace("State:\t", '')

def get_processes_list():            
    processes_list = []

    for process_id in os.listdir(PATH):
        if process_id.isdigit():
            cmd = get_cmd(process_id)
            if len(cmd) > 0:
                status = get_status(process_id)
                if status.startswith("R"):
                    processes_list.append(" ".join(status.split()) + " " + cmd)
    return processes_list
    
processes_list = get_processes_list()    
processes_list.sort()            
for line in processes_list:
    print(line)
