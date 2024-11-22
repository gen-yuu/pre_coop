from flask import Flask, render_template, request
from flask_socketio import SocketIO
import pika
import eventlet
from eventlet import wsgi
import json
import os
from utils.test_db import *

# Pythonの標準ライブラリを非同期I/Oに対応するように書き換えます。
#eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*",async_mode='threading')


def user_registration(nfc_id):
    data = {}
    data['nfcId']=nfc_id
    data['userName'] ='gennai'
    data["userYear"]= 2025
    data["balance"] = 0
    data["charge"] = 0
    new_user_or_update_user(data)

# Create a function to handle incoming RabbitMQ messages
def on_rabbitmq_message_user(body):
    # When a message is received, broadcast it to all connected WebSocket clients
    data = json.loads(body)
    socketio.emit('user_info', {'user_id': data[0], 'userName': data[1], 'nfc_id': data[2], 'grade': data[3], 'balance': data[4]})

def on_rabbitmq_message_user_registration(body):
    # When a message is received, broadcast it to all connected WebSocket clients
    data = json.loads(body)
    socketio.emit('user_nfc', {'nfc_id': data})
    user_registration(data)
    print("登録")


# Define a function to set up RabbitMQ connection and channel
def setup_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='nfc_queue')
    channel.queue_declare(queue='nfc_registration')
    
    # Set up consumers
    channel.basic_consume(queue='nfc_queue', on_message_callback=lambda ch, method, properties, body: on_rabbitmq_message_user(body), auto_ack=True)
    channel.basic_consume(queue='nfc_registration', on_message_callback=lambda ch, method, properties, body: on_rabbitmq_message_user_registration(body), auto_ack=True)
    return channel

# Create a separate thread for the RabbitMQ consumer
def rabbitmq_consumer_thread():
    print(" [*] Connecting to server ...")
    channel = setup_rabbitmq()
    print(" [*] Waiting for messages. To exit press Ctrl+C")
    channel.start_consuming()

def create_app():
    rabbitmq_consumer_thread()
    return app

if __name__ == '__main__':
    create_app()