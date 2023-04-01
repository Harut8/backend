import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
def send_company_zayavka_email(*, message_):
    """ FUNCTION FOR SENDING EMAIL"""
    try:
        from API_dir.api_creator import email_, email_pass
        sender_email = email_
        password = email_pass
        receiver_add = "kochkanyan@gmail.com"
        receiver_email = "kochkanyan@gmail.com"
        smtp_server = smtplib.SMTP("smtp.mail.ru", 587)
        smtp_server.starttls() #setting up to TLS connection
        ##############
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "ЗАЯВКА"
        msg['From'] = formataddr(("PCASSA MANAGER", sender_email))
        msg['To'] = receiver_email
        #smtp_server.starttls() #setting up to TLS connection
        smtp_server.login(sender_email, password) #logging into out email id
        text = "ЗАЯВКА"
        mes = message_
        html = f"""\
        <html>
          <head></head>
          <body>
                <h3><i>ФИО</i></h3> {mes.fio}
                </br>
                <h3><i>Номер телефона</i></h3> {mes.phone}
                </br>
                <h3><i>Email</i></h3> {mes.email}
                </br>
                <h3><i>Страна</i></h3> {mes.country}
                <h3><i>Название организации</i></h3> {mes.company_name}
                <h3><i>Количество сотрудников</i></h3> {mes.costumer_count}
                <h3><i>Коммнтарии</i></h3> {mes.comments}
          </body>
        </html>
        """ if mes.fio !=None else \
        f"""\
        <html>
          <head></head>
          <body>
                <h3><i>Номер телефона</i></h3> {mes.phone}
          </body>
        </html>
        """
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        # smtp_server.sendmail(sender_email,receiver_email, msg.as_string())
        # smtp_server.quit()
        print('SUCCESS EMAIL Sent')
        return True
    except Exception as e:
        print(e)
        return None


