import smtplib
import urllib.parse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from email.headerregistry import Address
from email.utils import formataddr

def generate_url(*, id_: str):
    """ GENERATE URL FOR VERIFYING ACCOUNT"""
    from API_dir.api_creator import host
    url = 'https://armenia.pcassa.ru:443/verify/?'
    params = {'token_verify': id_, 'data': 'JbbfghGVEVGEJKIJCVBEJGHEBEKKEHBHNKVIRH'}
    return url + urllib.parse.urlencode(params)


def send_verify_link(*, receiver_email: str, message: str):
    """ FUNCTION FOR SENDING EMAIL"""
    try:
        #7UN5m0AmvhwpsuqQLM9x
        #sender_email = 'account@pcassa.ru'
        #password = 'j_kgtZdp3N-#'
        #receiver_add = receiver_email
        #smtp_server = smtplib.SMTP_SSL("mail.pcassa.ru", 465)
        ##############
        from API_dir.api_creator import email_, password_
        receiver_add = receiver_email
        smtp_server = smtplib.SMTP("smtp.mail.ru", 587)
        smtp_server.starttls() #setting up to TLS connection
        ##############
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "VERIFY PCASSA ACCOUNT"
        msg['From'] = formataddr(("PCASSA MANAGER", email_))
        msg['To'] = receiver_email
        #smtp_server.starttls() #setting up to TLS connection
        smtp_server.login(email_, password_) #logging into out email id
        text = "ПОДТВЕРДИТЬ АККАУНТ PCASSA"
        link_for_verify = u'<a href="{mes}">НАЖМИТЕ, ЧТОБЫ ПОДТВЕРДИТЬ ВАШ АККАУНТ PCASSA </a>'.format(mes=message)
        html = f"""\
        <html>
          <head></head>
          <body>
                <h2 color='red'> PCASSA </h2>
                <p> ПОСЛЕ ПЕРЕХОДА ПО ЭТОЙ ССЫЛКЕ ВАШ АККАУНТ БУДЕТ ПОДТВЕРЖДЕН
</p>
               {link_for_verify}
          </body>
        </html>
        """
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        smtp_server.sendmail(email_, receiver_add, msg.as_string())
        smtp_server.quit()
        print('SUCCESS EMAIL Sent')
        return True
    except Exception as e:
        print(e)
        return False
