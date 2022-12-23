import smtplib
import urllib.parse
from email.mime.text import MIMEText


def generate_url(*, id):
    """ GENERATE URL FOR VERIFYING ACCOUNT"""
    url = 'http://192.168.0.104:8000/verify/?'
    params = {'temp_acc_id': id, 'date': 'TFVEVBJHBhbghefv87y7t'}
    return url + urllib.parse.urlencode(params)


def send_message(*, receiver_email: str, message: str):
    """ FUNCTION FOR SENDING EMAIL"""
    try:
        sender_email = 'testauthor96@mail.ru'
        password = '7UN5m0AmvhwpsuqQLM9x'
        receiver_add = receiver_email
        smtp_server = smtplib.SMTP("smtp.mail.ru", 587)
        smtp_server.starttls() #setting up to TLS connection
        smtp_server.login(sender_email, password) #logging into out email id
        #print(message)
        msg = MIMEText(u'<a href="{mes}">VERIFY EMAIL</a>'.format(mes=message), 'html')
        smtp_server.sendmail(sender_email, receiver_add, f"{msg}")
        smtp_server.quit()
        print('SUCCESS EMAIL Sent')
        return True
    except Exception as e:
        print('ERROR EMAIL Sent')
        return e

