#!/usr/bin/python3
import os
import sqlite3
import argparse
connection = sqlite3.connect('/var/serpent/jobs.db')
cursor = connection.cursor()
supported_types = ['py','sh','bin']
illegal_names = ['all']
func_names = ['all']
def register(name: str, delay: str, path: str, type: str):
    if path.startswith('./'):
        path = os.getcwd() + path.replace('./','/')
    print(path)
    if type not in supported_types:
        print('Type:',type,'not supported')
    else:
        if len(cursor.execute('select * from jobs where name=?',(name,)).fetchall()) == 0:
            if delay.endswith("s"):
                delay = int(delay[:-1])
            elif delay.endswith("m"):
                delay = int(delay[:-1]) * 60
            elif delay.endswith("h"):
                delay = int(delay[:-1]) * 3600
            elif delay.endswith("d"):
                delay = int(delay[:-1]) * 86400
            else:
                print(f"Invalid time format: {delay}")
            cursor.execute('insert into jobs values(?,?,?,0,?)',(name,delay,path,type))
            connection.commit()
        else:
            print('Job:',name,'already exists')


def remove(name: str):
    cursor.execute('delete from jobs where name=?',(name,))
    connection.commit()
    print('removed job:',name)

def activate(name: str):
    if len(cursor.execute('select * from jobs where name=?',(name,)).fetchall()) == 0:
        print('job:',name,'does not exist')
    else:
        cursor.execute('update jobs set staus=1 where name=?',(name,))
        connection.commit()
        print('job:',name,'activated')

def disable(name: str):
    if len(cursor.execute('select * from jobs where name=?', (name,)).fetchall()) == 0:
        print('job:', name, 'does not exist')
    else:
        cursor.execute('update jobs set staus=0 where name=?',(name,))
        connection.commit()
        print('job:', name, 'disabled')

def show(name: str):
    if name == 'all':
        for item in cursor.execute('select name from jobs;').fetchall():
            print(item[0])
    else:
        data = cursor.execute('select * from jobs where name=?;',(name,)).fetchone()
        state = data[3]
        match state:
            case 0:
                state = 'disabled'
            case 1:
                state = 'active'
        print('name:',data[0])
        print('delay:',str(data[1])+'s')
        print('file:',data[2])
        print('status:',state)
        print('filetype:',data[4])


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", required=True)

create_parser = subparsers.add_parser('create', help='used to create a new job')
create_parser.add_argument('-n','--name',help='name of your process')
create_parser.add_argument('-p','--path',help='path to file of your process')
create_parser.add_argument('-d','--delay',help='delay after which your process will be rerun')
create_parser.add_argument('-t','--type',help='file type of your process')

start_parser = subparsers.add_parser('enable', help='used to start a job')
start_parser.add_argument('-n','--name',help='name of your process')

disable_parser = subparsers.add_parser('disable', help='used to disable a job')
disable_parser.add_argument('-n','--name',help='name of your process')


remove_parser = subparsers.add_parser('remove', help='used to remove a job')
remove_parser.add_argument('-n','--name',help='name of your process')

restart_parser = subparsers.add_parser('restart', help='restarts the service (required if a new job is enabled)')
start_parser = subparsers.add_parser('start', help='starts the service')
stop_parser = subparsers.add_parser('stop', help='stops the service')
list_parser = subparsers.add_parser('list', help='lists all services')

args = parser.parse_args()

command = args.command
if command == 'create':
    c = 0
    if args.name is None:
        c = 1
        print('error: missing name')
    if args.delay is None:
        c = 1
        print('error: missing delay')
    if args.path is None:
        c = 1
        print('error: missing path')
    if args.type is None:
        c = 1
        print('error: missing type')
    if c == 0:
        register(args.name,args.delay,args.path,args.type)
        print(f'new job "{args.name}" added')

elif command == 'enable':
    c = 0
    if args.name is None:
        c = 1
        print('error: missing name')
    if c == 0:
        activate(args.name)
        print(f'job "{args.name}" started')

elif command == 'disable':
    c = 0
    if args.name is None:
        c = 1
        print('error: missing name')
    if c == 0:
        disable(args.name)
        print(f'job "{args.name}" stopped')

elif command == 'remove':
    c = 0
    if args.name is None:
        c = 1
        print('error: missing name')
    if c == 0:
        remove(args.name)
        print(f'job "{args.name}" removed')

elif command == 'restart':
    os.system('systemctl restart serpent.service')

elif command == 'stop':
    os.system('systemctl stop serpent.service')

elif command == 'start':
    os.system('systemctl start serpent.service')

