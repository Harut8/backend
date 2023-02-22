import smtplib
import urllib.parse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def generate_url_for_verify_tarif(*, order_id_token: str):
    """ GENERATE URL FOR VERIFYING ACCOUNT"""
    from API_dir.api_creator import host
    url = 'http://'+host+':8000/verifypayment/?'
    params = {'client_token': order_id_token}
    return url + urllib.parse.urlencode(params)


def send_order_verify_link_email(*, receiver_email: str, message: str):
    """ FUNCTION FOR SENDING EMAIL"""
    try:
        sender_email = 'testauthor96@mail.ru'
        password = '7UN5m0AmvhwpsuqQLM9x'
        receiver_add = receiver_email
        smtp_server = smtplib.SMTP("smtp.mail.ru", 587)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "VERIFY PCASSA TARIF"
        msg['From'] = sender_email
        msg['To'] = receiver_email
        smtp_server.starttls() #setting up to TLS connection
        smtp_server.login(sender_email, password) #logging into out email id
        text = "VERIFY PCASSA ACCOUNT"
        link_for_verify = u'<a href="{mes}">CLICK TO VERIFY YOUR PCASSA TARIF</a>'.format(mes=message)
        html = f"""\
        <html>
          <head></head>
          <body>
                <h2 color='red'> PCASSA </h2>
                <p> AFTER CLICKING TO THIS LINK YOUR ACCOUNT BE VERIFIED</p>
               {link_for_verify}
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
