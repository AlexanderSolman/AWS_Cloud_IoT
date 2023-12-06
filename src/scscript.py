import serial
import json
import datetime
import time
import boto3
import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Setup variables
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
data_topic = 'rock/device1'
root_ca = "/path/to/root-CA"
cert = "/path/to/thing.cert.pem"
private_key = "/path/to/thing.private.key"
endpoint = "your-endpoint"

# Connection configs
client = AWSIoTMQTTClient("thing")
client.configureEndpoint(endpoint, 8883)
client.configureCredentials(root_ca, private_key, cert)

# Connect to service, read measurements and publish data
try:
    client.connect()
    while True:
        temp = float(ser.readline().decode('utf-8').strip())
        hum = float(ser.readline().decode('utf-8').strip())
        timestamp = datetime.datetime.now().strftime("%m/%d/%Y, &H:%M:%S")

        if temp and hum:
            payload = {
                "timestamp": timestamp,
                "temperature": temp,
                "humidity": hum
            }
            
            try:
                client.publish(data_topic, json.dumps(payload), 1)
                print(f"Published {temp} and {hum} to topic: {data_topic}")
            except Exception as e:
                print(f"Publish failed: {e}")

except KeyboardInterrupt:
    print("Closing...")

finally:
    ser.close()
    client.disconnect()