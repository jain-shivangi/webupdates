#!/usr/bin/env python
__author__ = 'shivangi'

import sys
import smtplib
import json
from webupdates import get_updates
from webupdates.defaults import JSON_INPUT

# from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
    # from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)

    # old version
    # from email.MIMEText import MIMEText
from email.mime.text import MIMEText

# Get updates as dictionary
try:
    print("Getting updates...")
    updates = get_updates(json_input=JSON_INPUT)
except Exception as err:
    print("[ERROR] {0} - {1}".format(err.__class__.__name__, err.message))
    sys.exit(-1)

print("Got updates!")

print("Configuring mail...")
# Get mail configuration file
mail_details = {}
with open("subscriber.json") as fh:
    mail_details = json.load(fh)

if not mail_details:
    print("No subscriber.json file found!")
    sys.exit(-1)

#import pprint
#pprint.pprint(mail_details, indent=4)

# Set mailing attributes
try:
    pwd = mail_details["Sender"]["password"]
    from_ = mail_details["Sender"]["username"]
    to_ = mail_details["Subscribers"]
    mail_server = mail_details["Sender"]["smtp-server"]
    mail_port = mail_details["Sender"].get("smtp-port", 25)
except Exception as err:
    print("[ERROR] {0} - {1}".format(err.__class__.__name__, err.message))
    print("JSON not configured properly!")
    sys.exit(-1)

try:
    subject = mail_details["Subject"]
except:
    subject = "New updates found for"


def send_mail(user, pwd, from_, to_, subject, body, server, port=25):
    SMTPserver = server
    sender =     from_
    destination = to_

    USERNAME = user
    PASSWORD = pwd

    # typical values for text_subtype are plain, html, xml
    text_subtype = 'html'

    content = body

    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From']   = sender # some SMTP servers will do this automatically, not all

        s = smtplib.SMTP('smtp.vmware.com')
        # conn = SMTP(SMTPserver)
        # conn.set_debuglevel(True)
        # conn.login(USERNAME, PASSWORD)
        try:
            s.sendmail(sender, destination, msg.as_string())
        finally:
            s.quit()

    except Exception, exc:
        sys.exit( "mail failed; %s" % str(exc) ) # give a error message


print("Sending updates...")

for update_name, update_details in updates.items():
    sub = subject + " - {0}".format(update_name)
    # if not isinstance(update_details, list):
    #     update_details = [update_details]
    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')

    with open("zdnet-security", "r") as fh:
        body = fh.read()
    # body = "{0}\n".format("\n").join([r"{0}: {1}".format(k, v) for item in update_details for k, v in item.items()])
    send_mail(user=from_, pwd=pwd, from_=from_, to_=to_, subject=sub, body=body, server=mail_server, port=mail_port)

print("Sent all updates!")
print("Bye")