from influxdb import InfluxDBClient
import constants as CS
import time
import random

if __name__ == "__main__":
    client = InfluxDBClient(host = 'localhost', port = 8086, database = "tsdb")
    fields = {x: random.randint(0, 100) for x in CS.VARS_LIST}
    while True:
        client.write_points([
            {
                "measurement": "measurement_tsdb",
                "fields": fields
           }
        ])
        for element in fields:
            fields[element] += -1 + random.randint(0, 1)*2
        time.sleep(1)
