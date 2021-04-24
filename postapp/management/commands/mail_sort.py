import uuid

from django.core.management import BaseCommand
from doc.models import Document
from loan.models import Request
import email
import imaplib; imaplib.Debug = True
import os

from email.utils import parsedate_tz, parsedate_to_datetime
from django.conf import settings
from django.templatetags.tz import localtime
from django.utils.timezone import now

EXT_DCT = {
    'text/plain': 'txt',
    'image/webp': 'webp',
    'image/gif': 'gif',
    'text/html': 'html',
    'image/jpeg': 'jpg',
    'image/tiff': 'tiff',
    'image/png': 'png',
    'text/csv': 'csv',
    'application/ics': 'ics',
    'application/octet-stream': 'exe',
    'application/msword': 'docx',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'xml',
}


def save_attach(part, date_mail, folder_save):
    ext = EXT_DCT[part.get_content_type()]
    file_name = f"{date_mail.strftime('%Y-%m-%d-%H-%M-%S')}.{ext}"
    file_path = os.path.join(settings.EMAIL_FETCH.get['export_path'], file_name)
    with open(os.path.join(folder_save, file_name), 'wb') as f:
        f.write(part.get_payload(decode=1))
    return file_path


def get_mail():
    mail = imaplib.IMAP4_SSL(settings.EMAIL_FETCH['email_host'], 993)
    mail.login(settings.EMAIL_FETCH['email_user'], settings.EMAIL_FETCH['email_pass'])
    mail.list()
    # Выводит список папок в почтовом ящике.
    mail.select('inbox')
    # Возьмём непрочитанные сообщения
    result, data_b = mail.uid('search', None, 'SEEN')  # , 'UNSEEN'
    if not result == 'OK':
        return None

    uid_lst_b = data_b[0].split()
    print(uid_lst_b)
    # Нужны самые свежие непрочитанные письма
    from_mail_set = set()
    file_path = None
    body = None
    for latest_email_uid in reversed(uid_lst_b):
        # Помечаем прочитанным
        # mail.uid('STORE', latest_email_uid, '-FLAGS', '\SEEN')
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        email_message = email.message_from_bytes(data[0][1])
        date_mail = parsedate_to_datetime(email_message['Date'])
        subject_mail, from_mail = email.utils.parseaddr(email_message['From'])
        from_mail_set.add(from_mail)
        # если с неправльного ящика
        # if from_mail not in settings.EMAIL_FETCH['legal_from']:
        #     continue

        dst = from_mail.split('@')[1]
        msg1 = mail.create(dst)
        msg2 = mail.uid('COPY', latest_email_uid, dst)
        mov, data = mail.uid('STORE', latest_email_uid, '+FLAGS', '(\Deleted)')
        print(from_mail, msg1, msg2, mov, data)
        mail.expunge()
        # Сколько секунд назад пришло письмо
        total_seconds = (localtime(now()).replace(tzinfo=None) - date_mail.replace(tzinfo=None)).total_seconds()

        print(f'Subject: {subject_mail}')
        print(f'From: {from_mail}')
        print(f'Date: {date_mail}')
        print(f'Seconds ago: {total_seconds}')
        # Если очень давно, то прекращаем спрашивать
        if total_seconds > 24 * 60 * 60 * 30:
            continue

        # Проверим аттачи
        attachment_lst = email_message.get_payload()
        if isinstance(attachment_lst, str):
            continue

        for msg in attachment_lst:
            if msg is None:
                continue
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                folder_save = os.path.join(settings.EMAIL_FETCH['export_path'], settings.EMAIL_FETCH['email_user'],
                                           from_mail)
                if not os.path.exists(folder_save):
                    os.makedirs(folder_save)
                ext = EXT_DCT.get(part.get_content_type(), 000)
                file_name = date_mail.strftime(f'%Y-%m-%d-%H-%M-%S-{str(uuid.uuid4())}')
                with open(os.path.join(folder_save, f'{file_name}.{ext}'), 'wb') as f:
                    f.write(part.get_payload(decode=True))



class Command(BaseCommand):
    """
    Проверять почту, принимать документы от пользователей, чьи ящики есть в БО.
    Обработанные письма складывать в одну папку, необработанные в другую.

    Необходимо включить доступ небезопасным приложениям по ссылке
    https://myaccount.google.com/lesssecureapps

    Включить IMA
    https://mail.google.com/mail/u/3/#settings/fwdandpop

    Добавить пароль для приложения
    https://passport.yandex.com/profile/

    >> python manage.py mail_fetcher

    """
    help = 'Mail Fetcher'

    def handle(self, *args, **options):
        get_mail()
