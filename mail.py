import smtplib
smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
smtpobj.ehlo()
smtpobj.starttls()
smtpobj.ehlo()
smtpobj.login('***@gmail.com', 'Googleのパスワード')

from email.mime.text import MIMEText
from email.utils import formatdate
msg = MIMEText('こんにちは')
msg['Subject'] = 'タイトル'
msg['From'] = '***@gmail.com'
msg['To'] = '***@yahoo.co.jp'
msg['Date'] = formatdate()
sender_email = "***@gmail.com" 
receiver_email = "***@yahoo.co.jp" 
smtpobj.sendmail(sender_email, receiver_email, msg.as_string())
smtpobj.close()
print('mail sended!')
