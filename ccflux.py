import json

import influxdb
import serial
import untangle


with open('config.json', 'r') as fh:
    config = json.load(fh)


def get_data(port):
    ser = serial.Serial(port, 57600)
    xmldata = ser.readline()
    return xmldata


def parse_data(data):
    parsed = untangle.parse(data)
    return {
        'temperature': parsed.msg.tmpr.cdata,
        'watts': parsed.msg.ch1.watts.cdata
    }


def post_values(power):
    client = influxdb.InfluxDBClient(
        config['influxdb']['host'],
        config['influxdb']['port'],
        database=config['influxdb']['database']
    )
    points = [{'measurement': k, 'fields': {'value': v}}
              for k, v in power.items()]
    client.write_points(points)


if __name__ == "__main__":
    data = get_data()
    power = parse_data(data)
    post_values(power)
