import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_download_links(*, receiver_email: str, message: list):
    """ FUNCTION FOR SENDING EMAIL"""
    try:
        sender_email = 'testauthor96@mail.ru'
        password = 'DdTqUhyXiJ6FmMEZCVJN'
        receiver_add = receiver_email
        smtp_server = smtplib.SMTP("smtp.mail.ru", 587)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "DOWNLOAD PCASSA APPS"
        msg['From'] = sender_email
        msg['To'] = receiver_email
        smtp_server.starttls() #setting up to TLS connection
        smtp_server.login(sender_email, password) #logging into out email id
        text = "DOWNLOAD PCASSA APPS"
        link_for_desktop_cassa = u'<a href="{mes}">CLICK TO DOWNLOAD DESKTOP CASSA</a>'.format(mes=message[0])
        link_for_mobile_cassa = u'<a href="{mes}">CLICK TO DOWNLOAD MOBILE CASSA</a>'.format(mes=message[1])
        link_for_web_manager = u'<a href="{mes}">CLICK TO DOWNLOAD WEB MANAGER</a>'.format(mes=message[2])
        link_for_mobile_manager = u'<a href="{mes}">CLICK TO DOWNLOAD MOBILE MANAGER</a>'.format(mes=message[3])
        html = f"""\
        <html>
          <head></head>
          <body>
                <h2 color='red'> PCASSA </h2>
               {link_for_desktop_cassa if message[0] is not None else ''}
               </br>
               {link_for_mobile_cassa if message[1] is not None else ''}
               </br>
               {link_for_web_manager if message[2] is not None else ''}
               </br>
               {link_for_mobile_manager if message[3] is not None else ''}
          </body>
        </html>
        """
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        smtp_server.sendmail(sender_email, receiver_add, msg.as_string())
        smtp_server.quit()
        print('SUCCESS EMAIL Sent')
        return True
    except Exception as e:
        print(e)
        return False
