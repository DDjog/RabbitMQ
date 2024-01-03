from mongoengine import Document
from mongoengine.fields import BooleanField, EmailField, StringField


class Contact(Document):
    fullname = StringField()
    email = EmailField()
    sent = BooleanField(default=False)


def get_email_for_id(_id):
    _email_for_id = Contact.objects(pk=_id).first()

    return _email_for_id.email


def set_email_sent_flag_for_id(_id):
    Contact.objects(pk=_id).update(set__sent=True)


def delete_data():
    Contact.drop_collection()
