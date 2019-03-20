import json
import os
from pathlib import Path

import influxdb
import serial
import untangle


config_file_path = Path(os.path.realpath(__file__)) / 'config.json'

with open(config_file_path, 'r') as fh:
    config = json.load(fh)


def get_data(port):
    xmldata = port.readline()
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
    ser = serial.Serial(config['port'], 57600)
    while True:
        data = get_data(ser)
        power = parse_data(data)
        post_values(power)
