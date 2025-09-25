#!/usr/bin/env python3

import json
from pathlib import Path

Settings = {
    "mode":"port_map",
    "ip_map":{
        "ip_body":"10.20.30",
        "ip_start":200,
        "ip_end":300,
        "ip_step":10,
        "port":37000
    },
    "port_map":{
        "port_start":37000,
        "port_end":37900,
        "port_step":100,
        "ip":"10.20.30.100"
    },
    "output":"host"
}

def mode_ip():
    process = Settings["ip_map"]
    host_list = []
    for i in range(process["ip_start"], process["ip_end"]+1,process["ip_step"]):
        host_list.append(f"{process['ip_body']}.{i}")
    return host_list

def mode_port():
    process = Settings["port_map"]
    port_list = []
    for i in range(process["port_start"], process["port_end"]+1,process["port_step"]):
        port_list.append(f"{process['ip']}:{i}")
    return port_list

def save_data(list,path):
    path = Path(path)
    path.write_text('\n'.join(list) + '\n')
    print(f"[+] wrote {len(list)} hosts -> {path}")

if __name__ == "__main__":
    if Settings["mode"] == "ip_map":
        host = mode_ip()
    elif Settings["mode"] == "port_map":
        host = mode_port()
    save_data(host, Settings["output"])
        
