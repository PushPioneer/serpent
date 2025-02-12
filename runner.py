import os
import sqlite3
import subprocess
import time
import threading
import logging
import sys
connection = sqlite3.connect('/var/serpent/jobs.db')
cursor = connection.cursor()

jobs = cursor.execute('select * from jobs where staus=1;').fetchall()

def run_job(path: str, delay: int, type: str):
    prefix = ''
    print(type)
    if type == 'py':
        prefix = 'python3 '
    elif type == 'sh':
        prefix = 'bash '
    elif type == 'bin':
        pass
    while True:
        command = prefix+path
        logging.info(command)
        a = subprocess.call(command, shell=True)
        time.sleep(delay)
running = []
while True:
    logging.info('r')
    try:
        for job in jobs:
            name = job[0]
            delay = job[1]
            path = job[2]
            type = job[4]
            if name in running:
                print('no new jobs')
                logging.info('no new jobs')
            else:
                print('new job found')
                logging.info('new job found')
                running.append(name)
                thread = threading.Thread(target=run_job, args=(path, delay, type), name=name)
                thread.start()
    except Exception as e:
        logging.warning(e)
    time.sleep(5)