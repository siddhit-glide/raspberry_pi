import ssl
import paho.mqtt.client as mqtt

iot_endpoint = "azi6pydf2x48a-ats.iot.ap-south-1.amazonaws.com"
iot_port = 8883

cert_file = "/home/dell/certs/certificate.pem.crt"
key_file = "/home/dell/certs/private.pem.key"
ca_file = "/home/dell/certs/AmazonRootCA1.pem"

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected with reason code: {reason_code}")
    if reason_code == 0:
        client.subscribe("/test")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(ca_certs=ca_file, certfile=cert_file, keyfile=key_file, tls_version=ssl.PROTOCOL_TLS)

client.connect(iot_endpoint, iot_port, keepalive=60)
client.loop_forever()

