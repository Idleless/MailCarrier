Settings can either be set in the config.json or via the command line. Command line options takes priority over config.json

Example: ./mailCarrier.py --senderEmail 'sender@gmail.com' --receiverEmail 'rerciver@gmail.com' --runTest HelloWorldELF --whatIf False


Test cases are placed in a subfolder in the tests folder and must contain a test.json file.

format of test.json:<br />
  name = name of the test (sent in subject)<br />
  description =  description of the test (sent in body)<br />
  attachments = a list of files to attach to the email<br />
