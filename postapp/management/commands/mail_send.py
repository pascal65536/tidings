import os
from django.core.management import BaseCommand
from django.conf import settings
from django.core import mail
from django.conf import settings


class Command(BaseCommand):
    """
    Ппослать почту
    >> python manage.py mail_send

    """
    help = 'Mail Sender'

    def handle(self, *args, **options):
        mail_body = 'Body'
        with mail.get_connection() as connection:
            msg = mail.EmailMessage('Ошибки экспорта данных из файла',
                                    mail_body,
                                    settings.EMAIL_HOST_USER,
                                    [settings.EMAIL_TO],
                                    connection=connection)
            msg.content_subtype = "html"
            msg.send()
