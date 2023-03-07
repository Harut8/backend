import smtplib
import urllib.parse

def send_unique_id(*, receiver_email: str, message: str):
    """ FUNCTION FOR SENDING EMAIL"""
    try:
        sender_email = 'testauthor96@mail.ru'
        password = 'DdTqUhyXiJ6FmMEZCVJN'
        receiver_add = receiver_email
        smtp_server = smtplib.SMTP("smtp.mail.ru", 587)
        smtp_server.starttls() #setting up to TLS connection
        smtp_server.login(sender_email, password) #logging into out email id
        #print(message)
        smtp_server.sendmail(sender_email, receiver_add, f"{message}")
        smtp_server.quit()
        print('SUCCESS EMAIL Sent')
        return True
    except Exception as e:
        print(e)
        return False

