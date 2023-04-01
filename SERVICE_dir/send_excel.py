import os
import smtplib,ssl
import urllib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from email.utils import formataddr

def send_mail(send_to,order_id,subject='DOWNLOAD EXCEL',text='DOWNLOAD EXCEL',isTls=True):
    try:
        print(os.getcwd())
        #sender_email = 'account@pcassa.ru'
        #password = 'j_kgtZdp3N-#'
        #receiver_add = receiver_email
        #smtp_server = smtplib.SMTP_SSL("mail.pcassa.ru", 465)
        #smtp_server.starttls()  # setting up to TLS connection
        ##############
        sender_email = 'pcassa.manager@mail.ru'
        password = '9izMrHQdREq0PkBZtXyi'
        receiver_add = receiver_email
        smtp_server = smtplib.SMTP("smtp.mail.ru", 587)
        smtp_server.starttls() #setting up to TLS connection
        ##############
        msg = MIMEMultipart()
        msg['From'] = formataddr(("PCASSA MANAGER", sender_email))
        msg['To'] = send_to
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = subject
        f = f"SERVICE_dir/csv/{order_id}.xlsx"
        attachment = open(f, "rb")
        file_name = os.path.basename(f)
        msg.attach(MIMEText(text))
        part = MIMEApplication(attachment.read(), _subtype='xlsx')
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=file_name)
        msg.attach(part)
        smtp = smtplib.SMTP("smtp.mail.ru", 587)
        if isTls:
            smtp.starttls()
        smtp.login(sender_from,password)
        smtp.sendmail(sender_from, send_to, msg.as_string())
        smtp.quit()
        print("EXCEL SENDED")
        return True
    except Exception as e:
        print(e)
        return
