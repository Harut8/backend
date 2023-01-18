import smtplib
import random


def send_recovery_code(*, receiver_email: str):
    """ FUNCTION FOR SENDING EMAIL"""
    try:
        sender_email = 'testauthor96@mail.ru'
        password = '7UN5m0AmvhwpsuqQLM9x'
        receiver_add = receiver_email
        message = "".join([str(random.randint(0, 9)) for i in range(9)])
        smtp_server = smtplib.SMTP("smtp.mail.ru", 587)
        smtp_server.starttls() #setting up to TLS connection
        smtp_server.login(sender_email, password) #logging into out email id
        smtp_server.sendmail(sender_email, receiver_add, message)
        smtp_server.quit()
        print('SUCCESS EMAIL Sent')
        return message
    except Exception as e:
        print(e)
        return None


