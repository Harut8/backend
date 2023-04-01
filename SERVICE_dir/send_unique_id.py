from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import urllib.parse
from email.utils import formataddr

def send_unique_id(*, receiver_email: str, message: str):
    """ FUNCTION FOR SENDING EMAIL"""
    try:
        print(message)
        #sender_email = 'account@pcassa.ru'
        #password = 'j_kgtZdp3N-#'
        #receiver_add = receiver_email
        #smtp_server = smtplib.SMTP_SSL("mail.pcassa.ru", 465)
        ##############
        sender_email = 'pcassa.manager@mail.ru'
        password = 'YfpzwLkLCBAaS1ndJpqi'
        receiver_add = receiver_email
        smtp_server = smtplib.SMTP("smtp.mail.ru", 587)
        smtp_server.starttls() #setting up to TLS connection
        ##############
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "VERIFY PCASSA ACCOUNT"
        msg['From'] = formataddr(("PCASSA MANAGER", sender_email))
        msg['To'] = receiver_email
        #smtp_server.starttls() #setting up to TLS connection
        smtp_server.login(sender_email, password) #logging into out email id
        text = "VERIFY PCASSA ACCOUNT"
        link_for_verify = '<p>YOUR PCASSA ACCOUNT</p>'
        html = f"""\
        <html>
          <head></head>
          <body>
                <h2 color='red'> PCASSA </h2>
                {link_for_verify}
                {message}
          </body>
        </html>
        """
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        smtp_server.sendmail(sender_email, receiver_add, msg.as_string())
        smtp_server.quit()
        return True
    except Exception as e:
        print(e)
        return False

