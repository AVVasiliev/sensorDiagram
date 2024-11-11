import requests
import time
import random

address = 'http://127.0.0.1:5000/sensor'


def post_sensor_data():
    sensor_data = random.randint(120, 150)
    resp = requests.post(address, json={'value': sensor_data})
    print(resp.text)


if __name__ == '__main__':
    while True:
        post_sensor_data()
        time.sleep(3)
