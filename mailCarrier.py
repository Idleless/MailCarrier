#!/usr/bin/env python3

import smtplib, ssl, json, argparse, os, getpass

from time import sleep

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main():
    config = initConfig()
    initTests(config)
    runTests(config)

# DO NOT EDIT THIS
# Configuration changes should be made in your config.json file.
# These are fallback values if your config.json file is missing values.
DEFAULT_CONFIG={
    "useSSL": True,
    "requiresAuth": True,
    "sleep": 5,
    "whatIf": True,
    "testDir": "./tests/",
    "emailTemplate": "./emailTemplate.json",
    "config": "./config.json"
}


def initConfig():

    required = ["senderEmail", "senderPassword", "receiverEmail", "smtpServer"]

    parser = argparse.ArgumentParser(description='Email sending framework to verify perimeter security appliances')

    parser.add_argument('--senderEmail', help='Source email address')
    parser.add_argument('--senderPassword', help='Password for Source email address')
    parser.add_argument('--receiverEmail', help='Destination email address')
    parser.add_argument('--smtpServer', help='Server to send the email to')

    parser.add_argument('--useSSL', help='If SSL is needed to connect to the SMTP server. On by default')
    parser.add_argument('--requiresAuth', help='If requiresAuth is needed to connect to the SMTP server. On by default')
    parser.add_argument('--sleep', help='Delay between emails')
    #parser.add_argument('--jitter', help='Adds a random delay ontop of sleep upto "jitter"') #TODO
    parser.add_argument('--whatIf', help='Only output the messages to stdout (does not send the emails)')
    parser.add_argument('--testDir', help='Location of test cases')
    parser.add_argument('--emailTemplate', help='Location of emailTemplate')

    # CLI only options
    parser.add_argument('--config', help='Location of the config file', default=DEFAULT_CONFIG['config'])
    parser.add_argument('--runTest', nargs='+', help='Only run the specified tests')

    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

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

def runSingleTest(config, test, emailTemplate):
    try:
        with open(os.path.join(config['testDir'], test, "test.json")) as testJson:
            testConfig = json.load(testJson)
    except json.decoder.JSONDecodeError as e:
        print("Unable to run testcase '{}': {}".format(test, e))
        return


    print("Running testcase '{}'".format(testConfig['name']))

    subject = emailTemplate['subject'].format(title=testConfig['name'])
    body = emailTemplate['body'].format(description=testConfig['description'])
    sender = config['senderEmail']
    password = config['senderPassword']
    receiver = config['receiverEmail']
    server = config['smtpServer']
    useSSL = str(config.get('useSSL', DEFAULT_CONFIG['useSSL'])).lower() != 'false'
    requiresAuth = str(config.get('requiresAuth', DEFAULT_CONFIG['requiresAuth'])).lower() != 'false'
    attachments = testConfig['attachments']
    path = os.path.join(config.get('testDir', DEFAULT_CONFIG['testDir']), test)
    whatIf = str(config.get('whatIf', DEFAULT_CONFIG['whatIf'])).lower() != 'false'

    if (password is None or password == "") and not whatIf and requiresAuth:
        password = getpass.getpass("Password for {}: ".format(sender))
        config['senderPassword'] = password

    sendEmail(subject, body, sender, password, receiver, server, useSSL, requiresAuth, attachments, path, whatIf)


def runTests(config):

    if 'runTest' in config:
        tests = config['runTest']
    else:
        tests = os.listdir(config.get('testDir', DEFAULT_CONFIG['testDir']))

    with open(config.get('emailTemplate', DEFAULT_CONFIG['emailTemplate'])) as f:
        emailTemplate = json.load(f)

    first = True
    sleepTime = config.get('sleep', DEFAULT_CONFIG['sleep'])

    for test in tests:
        #ignore the template folder
        if test.startswith('_'):
            continue

        #Ugly hack to only sleep between sending emails
        if first:
            first = False
        else:
            print("Sleeping for", sleepTime)
            sleep(float(sleepTime))

        runSingleTest(config, test, emailTemplate)




# from: https://realpython.com/python-send-email/
def sendEmail(subject, body, sender, password, receiver, server, useSSL, requiresAuth, attachments, path, whatIf):
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
    if whatIf:
        print("Warning: Not sending due to WhatIf being true")
    else:
        if useSSL:
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(server, 465, context=context)
        else:
            server = smtplib.SMTP(server)

        if requiresAuth:
            server.login(sender, password)

        server.sendmail(sender, receiver, text)
        server.quit()

if __name__ == "__main__":
    main()
