# AWD Pwn

该脚本仅适用于AWD的Pwn，由``run.sh``依次驱动三个脚本，实现批量攻击、自动提交flag功能

## 目录结构

| 文件名          | 作用                                                         |
| --------------- | ------------------------------------------------------------ |
| init_host.py    | 初始化host，即ip和port，记录在host文件中                     |
| pwn_exp.py      | 读取host里的ip和port，多线程进行攻击，将flag记录在flag文件内 |
| submit.py       | 依次提交flag到目标url                                        |
| host            | 初始化的ip和port                                             |
| flag            | pwn_exp.py下获得的flag                                       |
| flag.submit.log | 提交flag的日志，记录状态                                     |

## 使用时需要修改的地方

### init_host.py

以下是需要修改的代码，部分无需修改的函数我就没展示了，只需要展示修改部分。后续同此

```python
Settings = {
    "mode":"port_map", #根据你的需要，看是使用变ip还是变port
    "ip_map":{
        "ip_body":"10.20.30", #根据网站题目的ip进行修改body,start,end
        "ip_start":200,
        "ip_end":300,
        "ip_step":10, #支持变步长，可修改
        "port":37000 #修改到题目固定的port
    },
    "port_map":{
        "port_start":37000, #根据题目的port修改start,end
        "port_end":37900,
        "port_step":100, #支持变步长，可修改
        "ip":"10.20.30.100" #修改到题目固定的ip
    },
    "output":"host" #输出的文件名，可自行修改
}

if __name__ == "__main__":
    if Settings["mode"] == "ip_map":
        host = mode_ip()
    elif Settings["mode"] == "port_map":
        host = mode_port()
    save_data(host, Settings["output"])
```

加入我的mode是``port_ip``，运行该脚本后，获得如下``host``

```
10.20.30.100:37000
10.20.30.100:37100
10.20.30.100:37200
10.20.30.100:37300
10.20.30.100:37400
10.20.30.100:37500
10.20.30.100:37600
10.20.30.100:37700
10.20.30.100:37800
10.20.30.100:37900
```

### pwn_exp.py

这是文件名，source_file是init_host.py里生成的文件名，flag_file是将获得的flag写入目的文件的文件名，均可自行修改

```python
flag_file = Path('flag')
source_file = Path('host')
```

这是实际执行exp的地方，将exp适配到该地区。记得自行修改成比赛的flag头，也可以自行设置timeout时间

```python
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

```

可自行修改并发线程数、超时时间和源路径

```python
def main():
    parser = argparse.ArgumentParser(description='pwn_exploit')
    parser.add_argument('-j','--jobs',type=int,default=10,help='并发线程数，默认10')
    parser.add_argument('-t','--timeout',type=int,default=10,help='每个任务超时时间，默认10s')
    parser.add_argument('--host',default=str(source_file),help='host文件路径，默认./host')
    args = parser.parse_args()
    run(Path(args.host),args.jobs,args.timeout)
```

### submit.py

flag_file同上，log_file是日志，日志名可以自己定。submit_url和token要根据比赛要求进行修改，有些可能还需要cookie，得自行添加进header里

```python
flag_file = Path("flag")
log_file = Path("flag.submit.log")
submit_url = "https://awd/api/flag" #example
token = "your_token"
REQUEST_TIMEOUT = 10

def submit_flag(session:requests.Session, flag:str, timeout:int=REQUEST_TIMEOUT):
    header = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {"flag":flag} #建议抓包查看payload格式
    try:
        p = session.post(submit_url, headers=header, json=payload, timeout=timeout)
        return True, p.status_code, p.text.strip()
    except requests.RequestException as e:
        return False, 0, str(e)
```

## 使用方法

```sh
chmod +x ./run.sh
./run.sh
```