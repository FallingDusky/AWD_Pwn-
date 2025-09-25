#!/bin/bash

Loop=300 
i=1

check_status() {
    if [ $? -ne 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Command failed: $1"
        return 1
    fi
    return 0
}

while true; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting new round $i..."
    
    chmod -R 777 ./
    check_status "chmod -R 777 ./"
    if [ $? -ne 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Failed to set file permissions. Retrying in 5 seconds..."
        sleep 5
        continue
    fi
    sleep 0.5
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Removing host and flag files..."
    rm -f host flag
    check_status "rm -f host flag"
    sleep 0.5
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Generating new host file..."
    python3 init_host.py
    check_status "python3 init_host.py"
    if [ $? -ne 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Failed to generate host file. Retrying in 5 seconds..."
        sleep 5
        continue
    fi
    sleep 0.5
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Running exploit script..."
    python3 pwn_exp.py
    check_status "python3 pwn_exp.py"
    if [ $? -ne 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Exploit script failed. Continuing with submission..."
    fi
    sleep 0.5
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Submitting flags..."
    python3 submit.py
    check_status "python3 submit.py"
    if [ $? -ne 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Flag submission failed. Retrying in 5 seconds..."
        sleep 5
        continue
    fi
    
    i=$((i+1))
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Round completed. Waiting for ${Loop} seconds..."
    sleep_time=$((Loop - 2)) 
    sleep $sleep_time
done
