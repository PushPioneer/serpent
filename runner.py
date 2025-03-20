import os
import sqlite3
import subprocess
import time
import threading
import logging
import sys
from datetime import datetime

logging.basicConfig(
    filename='/var/serpent/serpent.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

connection = sqlite3.connect('/var/serpent/jobs.db')
cursor = connection.cursor()

def get_dependencies(job_name):
    """Get list of dependencies for a job"""
    result = cursor.execute('SELECT dependencies FROM jobs WHERE name=?', (job_name,)).fetchone()
    if result and result[0]:
        return [d.strip() for d in result[0].split(',')]
    return []

def check_dependencies(job_name):
    """Check if all dependencies have completed successfully"""
    deps = get_dependencies(job_name)
    if not deps:
        return True
    
    for dep in deps:
        dep_job = cursor.execute('SELECT status, last_status FROM jobs WHERE name=?', (dep,)).fetchone()
        if not dep_job or dep_job[0] != 1:
            logging.info(f"Job {job_name} waiting for dependency {dep}")
            return False
        
        if not dep_job[1] or dep_job[1] != 'success':
            logging.info(f"Job {job_name} waiting for dependency {dep} to complete successfully")
            return False
    
    return True

def update_execution_history(job_name, status, error_message=None):
    """Update job execution history in the jobs table"""
    cursor.execute('''
        UPDATE jobs 
        SET last_run = ?, last_status = ?, last_error = ?
        WHERE name = ?
    ''', (datetime.now(), status, error_message, job_name))
    connection.commit()

def run_job(name: str, path: str, delay: int, type: str):
    prefix = ''
    logging.info(f"Starting job: {name}")
    
    if type == 'py':
        prefix = 'python3 '
    elif type == 'sh':
        prefix = 'bash '
    elif type == 'bin':
        pass
    
    while True:
        if not check_dependencies(name):
            logging.info(f"Job {name} waiting for dependencies")
            time.sleep(5)
            continue
            
        try:
            command = prefix + path
            logging.info(f"Executing command: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                status = 'success'
                logging.info(f"Job {name} completed successfully")
            else:
                status = 'failed'
                error_msg = result.stderr or "Unknown error"
                logging.error(f"Job {name} failed: {error_msg}")
            
            update_execution_history(name, status, result.stderr)
            
        except Exception as e:
            status = 'error'
            error_msg = str(e)
            logging.error(f"Job {name} encountered an error: {error_msg}")
            update_execution_history(name, status, error_msg)
        
        time.sleep(delay)

def get_active_jobs():
    """Get all active jobs from the database"""
    return cursor.execute('SELECT name, path, delay, type FROM jobs WHERE status=1').fetchall()

running = []
while True:
    try:
        jobs = get_active_jobs()
        for job in jobs:
            name, path, delay, type = job
            if name not in running:
                logging.info(f"Starting new job thread: {name}")
                thread = threading.Thread(
                    target=run_job,
                    args=(name, path, delay, type),
                    name=name
                )
                thread.start()
                running.append(name)
    except Exception as e:
        logging.error(f"Error in main loop: {e}")
    
    time.sleep(5)
