import configparser
import json
import mongoengine
import pika

config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

#mongo_url_local = "mongodb://localhost:27017/DBContacts"
mongo_url = f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority"""

rabbit_mq_url = "localhost"
rabbit_mq_url_port = 5672

mongoengine.connect( host = mongo_url )


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()


channel.exchange_declare(exchange='task_contact', exchange_type='direct')
channel.queue_declare(queue='contact_queue', durable=True)
channel.queue_bind(exchange='task_contact', queue='contact_queue')


def publish_message( _msg ):
    channel.basic_publish(
        exchange='task_contact',
        routing_key='contact_queue',
        body=json.dumps(_msg).encode(),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        )
    )