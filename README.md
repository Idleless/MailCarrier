# Running
Example: ./mailCarrier.py --senderEmail 'sender@gmail.com' --receiverEmail 'rerciver@gmail.com' --runTest HelloWorldELF --whatIf False

# Settings
Settings can either be set in the config.json or via the command line. Command line options takes priority over config.json

Options:
- senderEmail
- senderPassword (leave blank to enter via the command line)
- receiverEmail
- smtpServer
- sleep
- jitter (TODO)
- whatIf (Creates and prints the emails without sending them)
- testDir (directory that contains the test cases)
- emailTemplate (a json file that the emails are based on)
- runTest (Only runs the specified tests)

# Test Cases
Test cases are placed in a subfolder in the ./tests/ folder and must contain a test.json file.

format of test.json:
- name = name of the test (sent in subject)
- description = description of the test (sent in body)
- attachments = a list of files to attach to the email
