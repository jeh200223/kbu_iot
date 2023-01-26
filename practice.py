
import copy
import pprint
from datetime import datetime
import schedule
import time
from influxdb import InfluxDBClient

username = 'jeh'
password = 'jeh123'

database = 'my_test_db6'
retention_policy = 'autogen'

bucket = f'{database}/{retention_policy}'

# with InfluxDBClient(url='http://localhost:8086', token=f'{username}:{password}', org='signum') as ifdb:
# with InfluxDBClient(url='http://localhost:8086',  username=username, password=password) as ifdb:

ifdb = InfluxDBClient(host='34.64.88.253',  port=8086, username=username, password=password)

if True:
    ifdb.create_database(database)
    ifdb.get_list_database()

    # with client.write_api() as write_api:
    #     print('*** Write Points ***')
    #     point = Point("mem").tag("host", "host1").field("used_percent", 25.43234543)
    #     print(point.to_line_protocol())
    #     write_api.write(bucket=bucket, record=point)


    # print('*** Query Points ***')
    # query_api = client.query_api()
    # query = f'from(bucket: \"{bucket}\") |> range(start: -1h)'
    # tables = query_api.query(query)
    # for record in tables[0].records:
    #     print(f'#{record.get_time()} #{record.get_measurement()}: #{record.get_field()} #{record.get_value()}')


    points = [
    ]
    tablename = 'temper'
    fieldname = 'fld03'
    point = {
        "measurement": tablename,
        "tags": {
            "host": "server02",
            "region": "us-east"
        },
        "fields": {
            fieldname: 0
        },
        "time": None,
    }
    # dt = datetime.datetime.now() - datetime.timedelta(seconds=6)
    # ldt = utc_to_local(dt)
    # print ("UTC now=<%s> local now=<%s>" % (dt, ldt))

def while_schedule(): 
    dt = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    vals = [ 2.3, 1.7, 1.4, 0.7, 1.9 ]
    for v in vals:
        np = copy.deepcopy(point)
        np['fields'][fieldname] = v
        np['time'] = dt
        points.append(np)

        # points.append(
        #     Point(tablename)
        #     .tag("host","server02")
        #     .tag("region","us-east")
        #     .field("val",v)
        #     .time(int(dt.timestamp()))
        # )
        
    # ifdb.write_data(points)

    ifdb.write_points(points, database=database)

schedule.every(1).seconds.do(while_schedule)  

while True:
    schedule.run_pending()
    time.sleep(1)
    result = ifdb.query('select * from %s' % tablename, database=database)
    pprint.pprint(result.raw)
    