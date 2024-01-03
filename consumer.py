import json
import connect
import model


def sent_email(_id):
    print("sent email to: ", _id)

    email = model.get_email_for_id(_id)
    print("email sent: ", email)

    model.set_email_sent_flag_for_id(_id)


def processing_message(ch, method, properties, body):
    message = json.loads(body.decode())
    print(f" [x] MSG data rcs: {message}")
    sent_email(message['id'])
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    print('Odbieranie komunikatów, aby zakończyć program naciśnij CTRL+C')

    connect.channel.basic_qos(prefetch_count=1)
    connect.channel.basic_consume(queue='contact_queue', on_message_callback=processing_message)

    connect.channel.start_consuming()
