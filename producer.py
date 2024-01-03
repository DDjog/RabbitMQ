import faker

import connect
import model

NUMBER_OF_CONTACT = 10


def create_data(_seed=1234):
    fake_names = []
    fake_emails = []

    fake = faker.Faker()
    faker.Faker.seed(_seed)

    for _ in range(NUMBER_OF_CONTACT):
        fake_names.append(fake.name())
        fake_emails.append(fake.email())

    return fake_names, fake_emails


def put_data_to_mongo(_names, _emails):
    for idx in range(NUMBER_OF_CONTACT):
        c = model.Contact()
        c.fullname = _names[idx]
        c.email = _emails[idx]
        c.sent = False
        c.save()


def sent_message_to_rabbitmq():
    contacts = model.Contact.objects()
    for c in contacts:
        contact = {}
        contact['id'] = str(c.id)
        connect.publish_message(contact)


if __name__ == "__main__":
    model.delete_data()
    fn, fe = create_data()
    put_data_to_mongo(fn, fe)
    sent_message_to_rabbitmq()
