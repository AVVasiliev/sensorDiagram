from flask import Flask, request, jsonify
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# InfluxDB configuration
bucket = "energySensor"
org = "GTNH"
token = "XVlFUHdiripMWn32l1O0f64b7V2FaTKVYfWaBaAjBMGb_rE9MWRS5qXObqdZ_0L3I2LoQcRTrEksi8lQOU1Ejg=="
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)


@app.route('/sensor', methods=['POST'])
def collect_data():
    data = request.json
    sensor_id = 1 #data.get('sensor_id')
    value = data.get('value')

    # Create a point to write to InfluxDB
    point = influxdb_client.Point("sensor_data").tag("sensor_id", sensor_id).field("value", value)

    # Write the point to InfluxDB
    write_api.write(bucket=bucket, org=org, record=point)

    return jsonify({"status": "success", "sensor_id": sensor_id, "value": value}), 201


@app.route('/data', methods=['GET'])
def get_data():
    query_api = client.query_api()
    query = f'from(bucket:"{bucket}") |> range(start: -1m) |> filter(fn: (r) => r._measurement == "sensor_data")'
    result = query_api.query(query=query, org=org)

    data_points = []
    for table in result:
        for record in table.records:
            data_points.append({
                "time": record.get_time().isoformat(),
                "sensor_id": record.values.get('sensor_id'),
                "value": record.get_value()
            })

    return jsonify(data_points), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
