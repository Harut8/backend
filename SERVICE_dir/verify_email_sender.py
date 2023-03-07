import smtplib
import urllib.parse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def generate_url(*, id_: str):
    """ GENERATE URL FOR VERIFYING ACCOUNT"""
    from API_dir.api_creator import host
    url = 'http://'+host+':8000/verify/?'
    params = {'token_verify': id_, 'data': 'JbbfghGVEVGEJKIJCVBEJGHEBEKKEHBHNKVIRH'}
    return url + urllib.parse.urlencode(params)


def send_verify_link(*, receiver_email: str, message: str):
    """ FUNCTION FOR SENDING EMAIL"""
    try:
        #7UN5m0AmvhwpsuqQLM9x
        sender_email = 'testauthor96@mail.ru'
        password = 'DdTqUhyXiJ6FmMEZCVJN'
        receiver_add = receiver_email
        smtp_server = smtplib.SMTP("smtp.mail.ru", 587)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "VERIFY PCASSA ACCOUNT"
        msg['From'] = sender_email
        msg['To'] = receiver_email
        smtp_server.starttls() #setting up to TLS connection
        smtp_server.login(sender_email, password) #logging into out email id
        text = "VERIFY PCASSA ACCOUNT"
        link_for_verify = u'<a href="{mes}">CLICK TO VERIFY YOUR PCASSA ACCOUNT</a>'.format(mes=message)
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
