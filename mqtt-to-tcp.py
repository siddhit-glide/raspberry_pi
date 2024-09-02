import ssl
import socket
import paho.mqtt.client as mqtt

# AWS IoT Core settings
iot_endpoint = "azi6pydf2x48a-ats.iot.ap-south-1.amazonaws.com"
iot_port = 8883

# Paths to certificate files
cert_file = "/home/dell/certs/certificate.pem.crt"
key_file = "/home/dell/certs/private.pem.key"
ca_file = "/home/dell/certs/AmazonRootCA1.pem"

# TCP server settings
tcp_server_ip = "192.168.103.185"  # Replace with your TCP server IP
tcp_server_port = 4040          # Replace with your TCP server port

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected with reason code: {reason_code}")
    if reason_code == 0:
        client.subscribe("/test")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received message: {message} on topic {msg.topic}")

    # Send the received message to the TCP server
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            tcp_socket.connect((tcp_server_ip, tcp_server_port))
            tcp_socket.sendall(message.encode())
            print("Message sent to TCP server.")
    except Exception as e:
        print(f"Error sending message to TCP server: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(ca_certs=ca_file, certfile=cert_file, keyfile=key_file, tls_version=ssl.PROTOCOL_TLS)
client.connect(iot_endpoint, iot_port, keepalive=60)
client.loop_forever()


