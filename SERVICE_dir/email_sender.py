import smtplib
import urllib.parse


def generate_url(*, name):
    url = 'http://127.0.0.1:8000/verify/?'
    params = {'temp_acc_id': name, 'temp_acc_status': 1}
    print(url + urllib.parse.urlencode(params))


def send_message(*, receiver_email: str, message: str):
    try:
        sender_email = 'mavetisyan461@gmail.com'
        password = 'd197936a'
        receiver_add = receiver_email
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls() #setting up to TLS connection
        smtp_server.login(sender_email, password) #logging into out email id
        msg_to_be_sent = message
        smtp_server.sendmail(sender_email, receiver_add, msg_to_be_sent)
        smtp_server.quit()
        return True
    except Exception as e:
        return e
