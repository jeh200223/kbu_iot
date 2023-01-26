from tkinter import *
import tkinter as tk
from datetime import datetime
from influxdb import InfluxDBClient
import schedule
import time
import numpy as np

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


def temax_scale():

 global temax_value
 temax_value = str(temp_max.get())


def temin_scale():

 global temin_value
 temin_value = str(temp_min.get())


def humax_scale():

  global humax_value
  humax_value = str(humi_max.get())


def humin_scale():

  global humin_value
  humin_value = str(humi_min.get())


temp_val = np.array ([2.3, 3.2, 4.8, 5.9, 12.0], dtype = float)  
def while_schedule(): 
    a = 0
    while a <= 3:
        a += 1
    client = get_influxdb(database_name='my_test_db6', host='34.64.88.253', port=8086)
    client.get_list_database()
    client.get_list_measurements
    points = [{'measurement':'temper',
     'tags':{'server_id': 'server1'}, 
     'fields':{ 'v' : temp_val[a] },
     'time': datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")}] 
    client.write_points(points=points, protocol='json')
    rs = client.query("""
    SELECT *
    FROM temper
    """)
    for point in rs.get_points():
        print(point)

schedule.every(1).seconds.do(while_schedule)

def btn_cmd():
    
    temax_scale()
    temin_scale()
    humax_scale()
    humin_scale()
    while True:
        schedule.run_pending()
        time.sleep(1)

    # get_influxdb()    
    # client = get_influxdb(database_name='ig_test333', host='34.64.88.253', port=8086)
    # client.get_list_database()
    # client.get_list_measurements
    # points = [{'measurement':'temp', 
    #  'tags':{'server_id': 'server1'}, 
    #  'fields':{'temp': 8.0 ,'humi': 9},
    #  'time': datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")}, # 한국시간 6시
    # {'measurement':'temp', 
    #  'tags':{'server_id': 'server1'}, 
    #  'fields':{'v': 10.0},
    #  'time': '2023-01-17 07:00:00+09:00'}, # 한국시간 7시
    # {'measurement':'temp', 
    #  'tags':{'server_id': 'server1'}, 
    #  'fields':{'v': 9.5},
    #  'time': '2023-01-17 08:00:00+09:00'}] # 한국시간 8시
    # client.write_points(points=points, protocol='json')
    # rs = client.query("""
    # SELECT max(v) as cnt_v
    # FROM temp 
    # WHERE time >= now() - 12h GROUP BY time(3h)
    # """)
    # for point in rs.get_points():
    #     print(point)


temp = tk.Tk()
temp.title("온습도 측정기")
temp.geometry("600x500")

l1 = Label(temp, text="전송 시간 간격")
l2 = Label(temp, text="온도설정  ")
l3 = Label(temp, text="MAX")
l4 = Label(temp, text="MIN")
l5 = Label(temp, text="습도설정")
l6 = Label(temp, text="MAX")
l7 = Label(temp, text="MIN")

l1.grid(row=0, column=0)
l2.grid(row=0, column=3)
l3.grid(row=1, column=3)
l4.grid(row=3, column=3)
l5.grid(row=0, column=4)
l6.grid(row=1, column=4)
l7.grid(row=3, column=4)


temp_max = Scale(temp, from_=-15, to=50)
temp_max.grid(row=2, column=3)
temp_min = Scale(temp, from_=-20, to=45)
temp_min.grid(row=4, column=3)

humi_max = Scale(temp, from_=0, to=100)
humi_max.grid(row=2, column=4)
humi_min = Scale(temp, from_=0, to=100)
humi_min.grid(row=4, column=4)
hour_var = tk.IntVar()
button_hour1 = tk.Radiobutton(temp, text="5분", value=1,
                              variable=hour_var)
button_hour1.grid(row=1, column=0)
button_hour2 = tk.Radiobutton(temp, text="10분", value=2,
                              variable=hour_var)
button_hour2.grid(row=2, column=0)
button_hour3 = tk.Radiobutton(temp, text="1시간", value=3,
                              variable=hour_var)
button_hour3.grid(row=3, column=0)


btn = Button(temp, text="데이터 전송", command=btn_cmd)

btn.grid(row=4, column=2)
temp.mainloop()