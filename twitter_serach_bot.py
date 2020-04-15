import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import json, time
from requests_oauthlib import OAuth1Session
from jinja2 import Environment, BaseLoader
from email.mime.multipart import MIMEMultipart


# Twitter API
API_KEY = "AYHDHrOF2VBWzDjMYZ5m6G7BC"
API_SECRET = "KVQSj4jiTcX9Z33oVpYGThcfwK4mWt2mKX4uFb5pvoQYJ37qlJ"
TOKEN = "2596440072-FZlZMabofR8izxDDUjPO3RUf7i8xozsVM1tFZ6k"
TOKEN_SECRET = "beXDRO4FH4gXCN8xuWgrSREUdbx4Omxw9nyiWsc1P7Azp"
API_Plan_Standard = "https://api.twitter.com/1.1/search/tweets.json?q="
limit_get_data_per_time = 30
what_type_result_data = "resent"  # mixed, recent, popular
mytwitter = OAuth1Session(API_KEY, API_SECRET, TOKEN, TOKEN_SECRET)

API_Plan_Standard = "https://api.twitter.com/1.1/search/tweets.json?q="
how_many_get_data = 30
what_type_result_data = "resent"  # mixed, recent, popular
search_keyword = "安倍晋三"

while True:
    url = API_Plan_Standard + search_keyword + "&result_type=" + what_type_result_data + "&count=" + str(how_many_get_data)
    response = mytwitter.get(url)
    response_data = json.loads(response.text)
    how_many_do_you_have = response_data['search_metadata']['count']
    print('items = ' + str(how_many_do_you_have))

    loop_counter = 0
    who = []
    when = []
    what = []
    twitter_url= []

    while loop_counter < how_many_do_you_have:
        first_data = response_data['statuses'][loop_counter]
        who.append(first_data['user']['name'])
        when.append(first_data['created_at'][:16])
        what.append(first_data['text'])
        twitter_url.append('https://twitter.com/oshimamarasa/status/' + str(first_data['id']))
        loop_counter += 1

    data_list = zip(who, when, what, twitter_url)
    context = {'data_list':data_list}

    # mail
    html_template = """\
    <p>つぶやかれています。</p>
    {% for d in data_list %}
        <li>who; {{ d.0 }}</li>
        <li>when; {{ d.1 }}</li>
        <li>what; {{ d.2 }}</li>
        <li>url; {{ d.3 }}</li>
        <hr>
    {% endfor %}
    """

    text_template = """\
    つぶやかれています。
    {% for d in data_list %}
        who ; {{ d.0 }}
        when ; {{ d.1 }}
        what ; {{ d.2 }}
        url ; {{ d.3 }}
        
    {% endfor %}
    """
    
    template = Environment(loader=BaseLoader).from_string(html_template)
    template2 = Environment(loader=BaseLoader).from_string(text_template)
    html_out = template.render(context)
    text_out = template2.render(context)

    # メール機能
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(' ***@gmail.com', 'google password')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'つぶやかれてますよ'
    msg['From'] = ' ***@yahoo.co.jp'
    msg['To'] = ' ***@gmail.com'
    #print(msg)
    sender_email = " ***@gmail.com"  # Enter your address
    receiver_email = " ***@yahoo.co.jp"  # Enter receiver address
    part1 = MIMEText(text_out, 'plain')
    part2 = MIMEText(html_out, 'html')
    msg.attach(part1)
    msg.attach(part2)
    smtpobj.sendmail(sender_email, receiver_email, msg.as_string())
    smtpobj.close()
    
    print('mail sended!')
    time.sleep(10)
