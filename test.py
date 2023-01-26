from tkinter import *
import tkinter as tk
from datetime import datetime
from influxdb import InfluxDBClient
import schedule
import time
from random import random

def get_influxdb(database_name, host='localhost', port=8086):
    client = InfluxDBClient(host, port)
    try:
        client.create_database(database_name)
        print('create ' + database_name)
    except Exception as e:
        print('create except')
        print(e)
        pass
    try:
        client.switch_database(database_name)
        print('switch ' + database_name)
    except Exception as e:
        print('switch except')
        print(e)
        return None
    return client

client = get_influxdb(database_name='my_test_db6', host='34.64.88.253', port=8086)
client.get_list_database()
client.get_list_measurements

def while_schedule():
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    points = [{'measurement':'temper', 
    'tags':{'server_id': 'server1'}, 
    'fields':{'v' : -5.0 },
    'time': current_time }] # 한국 현재시간

    client.write_points(points=points, protocol='json')

    rs = client.query("""
    SELECT *
    FROM temper
    """)

    for point in rs.get_points():
        print(point)

    client.write_points(points=points, protocol='json')

schedule.every(1).seconds.do(while_schedule)  

while True:
    schedule.run_pending()
    time.sleep(1)