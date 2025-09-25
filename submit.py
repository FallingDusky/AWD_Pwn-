from pathlib import Path
import time
import sys
import requests

flag_file = Path("flag")
log_file = Path("flag.submit.log")
submit_url = "https://awd/api/flag" #example
token = "your_token"
REQUEST_TIMEOUT = 10

def append_log(line:str):
    with open(log_file, "a") as f:
        f.write(line + "\n")

def submit_flag(session:requests.Session, flag:str, timeout:int=REQUEST_TIMEOUT):
    header = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {"flag":flag}
    try:
        p = session.post(submit_url, headers=header, json=payload, timeout=timeout)
        return True, p.status_code, p.text.strip()
    except requests.RequestException as e:
        return False, 0, str(e)

def main():
    if not flag_file.exists():
        print("No flag file found.")
        sys.exit(1)
    session = requests.Session()
    line_list = flag_file.read_text(encoding="utf-8").splitlines()

    total,success,fail = 0,0,0

    for each_line in line_list:
        flag = each_line.strip()
        if not flag:
            continue
        total += 1
        Now = time.strftime("%Y-%m-%d %H:%M:%S")
        consequence, status_code, response = submit_flag(session,flag)
        if consequence and status_code is not None:
            log_line = f"{Now} | {flag} -> HTTP {status_code} | {response}"
            print(f"[OK] {flag} -> HTTP {status_code}")
            success += 1
        else:
            log_line = f"{Now} | {flag} -> ERR | {response}"
            print(f"[FAIL] {flag} -> {response}")
            fail += 1
        append_log(log_line)
    print(f"[+] done. total={total} success={success} fail={fail}")
    print(f"[+] full log -> {log_file}")

if __name__ == "__main__":
    main()

