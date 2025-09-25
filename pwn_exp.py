from pwn import *
from pathlib import Path
from typing import Tuple, Optional
import sys
import argparse
import time
import threading
import concurrent.futures

context.log_level='error'

flag_file = Path('flag')
source_file = Path('host')
lock = threading.Lock()

def write_flag(flag:str):
    if not flag:
        return
    with lock:
        with open(flag_file, 'a') as f:
            f.write(flag.strip()+'\n')

def parse_host_line(line:str) -> Tuple[str, int]:
    if not line:
        return None
    strings = line.strip()
    if not strings or strings.startswith('#'):
        return None
    if ':' not in strings:
        return None
    try:
        ip,port = strings.split(':',1)
        ip = ip.strip()
        port = int(port.strip())
        return ip,port
    except ValueError:
        return None

def exploit(ip:str,port:int)->str:
    try:
        p = remote(ip,port,timeout=5)
        '''your exp,you need to change this area
        for example'''
        # p.sendlineafter(b'\n',b'cat flag')
        # data = p.recvuntil(b'}',timeout=3).decode()
        # if 'flag{' in data:
        #     start = data.find('flag{')
        #     end = data.find('}',start)
        #     if end != -1:
        #         return data[start:end+1]
        return ''
    except Exception as e:
        print(f"Connection to {ip}:{port} failed: {e}")
        return ''

def attack_in_thread(addr:Tuple[str,int])->Tuple[str,int]:
    ip,port = addr
    addr_str = f'{ip}:{port}'
    print(f'attack {addr_str}')
    try:
        flag = exploit(ip,port)
        if flag:
            write_flag(flag)
            return addr_str,f"Here is the flag:{flag}"
        else:
            return addr_str,"Something wrong, There has no flag"
    except Exception as e:
        return addr_str,f"ERROR:{e}"

def run(host_path:Path,jobs:int,timeout:int):
    if not host_path.exists():
        print(f'host file {host_path} not exists')
        return
    addr_list = []
    with open(host_path,'r') as f:
        for line in f:
            host_port = parse_host_line(line)
            if host_port:
                addr_list.append(host_port)
    if not addr_list:
        print('no host found')
        return
    print(f'[+] {len(addr_list)} hosts parsed,starting attack (jobs={jobs},timeout={timeout}s)')
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        key_to_addr = {executor.submit(attack_in_thread,each_addr): each_addr for each_addr in addr_list}
        for key in concurrent.futures.as_completed(key_to_addr):
            addr = key_to_addr[key]
            addr_string = f'{addr[0]}:{addr[1]}'
            try:
                result = key.result(timeout=timeout)
                print(f'{addr_string} {result[1]}')
            except concurrent.futures.TimeoutError:
                print(f'{addr_string} timeout')
            except Exception as e:
                print(f'{addr_string} error:{e}')
    cost = time.time()-start_time
    print(f'[+] attack finished,cost {cost}s')

def main():
    parser = argparse.ArgumentParser(description='pwn_exploit')
    parser.add_argument('-j','--jobs',type=int,default=10,help='并发线程数，默认10')
    parser.add_argument('-t','--timeout',type=int,default=10,help='每个任务超时时间，默认10s')
    parser.add_argument('--host',default=str(source_file),help='host文件路径，默认./host')
    args = parser.parse_args()
    run(Path(args.host),args.jobs,args.timeout)

if __name__ == '__main__':
    main()




