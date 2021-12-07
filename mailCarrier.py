#!/usr/bin/env python3

import smtplib, ssl, json, argparse, os

from time import sleep

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main():
    config = initConfig()
    initTests(config)
    runTests(config)


def initConfig():

    required = ["redEmail", "redPassword", "blueEmail"]

    with open("./config.json") as f:
        config = json.load(f)

    parser = argparse.ArgumentParser(description='Email sending framework to verify perimeter security appliances')

    parser.add_argument('--redEmail', help='Source email address')
    parser.add_argument('--redPassword', help='Password for Source email address')
    parser.add_argument('--blueEmail', help='Destination email address')

    parser.add_argument('--sleep', help='Delay between emails')
    parser.add_argument('--jitter', help='Adds a random delay ontop of sleep upto "jitter"')
    parser.add_argument('--whatIf', help='Only output the messages to stdout (does not send the emails)')
    parser.add_argument('--testDir', help='Location of test cases')
    parser.add_argument('--emailTemplate', help='Location of emailTemplate')

    #parser.add_argument('--runTest', help='Only run the specified tests')

    args = parser.parse_args()

    for key,value in vars(args).items():
        if not value is None:
            config[key] = value

    for req in required:
        if not req in config or config[req] is None:
            print("Error: missing arg for", req)
            print()
            parser.print_help()
            exit()

    return config

def initTests(config):
    pass

def runTests(config):
    tests = os.listdir(config['testDir'])

    with open(config['emailTemplate']) as f:
        emailTemplate = json.load(f)

    first = True

    for test in tests:
        #ignore the template folder
        if test.startswith('_'):
            continue

        try:
            with open(os.path.join(config['testDir'], test, "test.json")) as testJson:
                testConfig = json.load(testJson)
        except json.decoder.JSONDecodeError as e:
            print("Unable to run testcase '{}': {}".format(test, e))
            continue

        print("Running testcase '{}'".format(testConfig['name']))


        #Ugly hack to only sleep between sending emails
        if first:
            first = False
        else:
            sleep(config['sleep'])

        subject = emailTemplate['subject'].format(title=testConfig['name'])
        body = emailTemplate['body'].format(description=testConfig['description'])
        sender = config['redEmail']
        password = config['redPassword']
        receiver = config['blueEmail']
        attachments = testConfig['attachments']
        path = os.path.join(config['testDir'], test)
        whatIf = config['whatIf']
        sendEmail(subject, body, sender, password, receiver, attachments, path, whatIf)


# from: https://realpython.com/python-send-email/
def sendEmail(subject, body, sender, password, receiver, attachments, path, whatIf):
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    #message["Bcc"] = receiver_email

    message.attach(MIMEText(body, "plain"))

    for filename in attachments:
        with open(os.path.join(path,filename), "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        message.attach(part)

    text = message.as_string()

    print(text)
    if not whatIf:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)

if __name__ == "__main__":
    main()
