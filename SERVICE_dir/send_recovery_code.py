import smtplib
import random


def send_recovery_code(*, receiver_email: str):
    """ FUNCTION FOR SENDING EMAIL"""
    try:
        #sender_email = 'account@pcassa.ru'
        #password = 'j_kgtZdp3N-#'
        #receiver_add = receiver_email
        #smtp_server = smtplib.SMTP_SSL("mail.pcassa.ru", 465)
        ##############
        from API_dir.api_creator import email_, email_pass
        sender_email = email_
        password = email_pass
        receiver_add = receiver_email
        smtp_server = smtplib.SMTP("smtp.mail.ru", 587)
        smtp_server.starttls() #setting up to TLS connection
        ##############
        message = "".join([str(random.randint(0, 9)) for i in range(9)])
        #smtp_server = smtplib.SMTP("smtp.mail.ru", 587)
        #smtp_server.starttls() #setting up to TLS connection
        smtp_server.login(sender_email, password) #logging into out email id
        smtp_server.sendmail(sender_email, receiver_add, message)
        smtp_server.quit()
        print('SUCCESS EMAIL Sent')
        return message
    except Exception as e:
        print(e)
        return None


