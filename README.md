# Running
Example:<br />
`./mailCarrier.py --senderEmail sender@gmail.com --receiverEmail rerciver@gmail.com --runTest HelloWorldELF --whatIf False`

# Settings
Settings can either be set in the config.json or via the command line. Command line options takes priority over config.json

Options:
- senderEmail
- senderPassword (leave blank to enter via the command line)
- receiverEmail
- smtpServer
- useSSL (On by default)
- requiresAuth (On by default)
- sleep
- jitter (TODO)
- whatIf (Creates and prints the emails without sending them. On by default)
- testDir (directory that contains the test cases)
- emailTemplate (a json file that the emails are based on)
- runTest (Only runs the specified tests)

# Test Cases
Test cases are placed in a subfolder in the ./tests/ folder and must contain a test.json file.<br />
Any folders in ./tests/ that starts with \"_\" are ignored.

format of test.json:
- name = name of the test (sent in subject)
- description = description of the test (sent in body)
- attachments = a list of files to attach to the email

# Google 2FA workaround
If you're using a google account with 2FA, you will need to create an AppPassword. This is a randomly generated password that allows logging in without 2FA. I wouuld not recommend keeping this password for a long period of time and would recommend deleting the password from your account as soon as it is no longer needed.
https://myaccount.google.com/u/1/apppasswords
