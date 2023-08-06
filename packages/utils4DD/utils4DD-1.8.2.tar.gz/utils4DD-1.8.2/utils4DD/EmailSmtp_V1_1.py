#!/bin/python
# -*- coding: utf-8 -*-

# Class to send emails
###################
# EmailSmtp class #
###################
# Class for sending emails with attachments
class EmailSmtp:

    import os
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.utils import COMMASPACE
    from email import encoders

    host = None
    port = 25
    user = None
    password = None
    isTls = False

    # Constructor
    def __init__(self, host='127.0.0.1', port=25, user=None, password=None, isTls=False):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.isTls = isTls

    # Send a email with the possibility to attach one or several  files
    def sendMessage(self, fromAddr, toAddrs, subject, content, files=None):
        '''
        Send an email with attachments.

        - Configuring:
            smtp = EmailSmtp()
            smtp.host = 'smtp.office365.com'
            smtp.port = 587
            smtp.user = "datalab@akka.eu"
            smtp.password = "xxxxx"
            smtp.isTls = True

        - Examples of contents:
            # A pure text content
            content1 = "An alert level 3 has been created from the system"
            # Another pure text content
            content2 = [["An alert level 3 has been created from the system", "text"]]
            # A pure html content
            content3 = [["An alert level 3 has been created <br>from the system.<br>", "html"]]
            # A list of text and html contents
            content4 = [
                ["ALERT LEVEL 3!\n", "text"],
                ["An alert level 3 has been created <br>from the system.<br><br>", "html"],
                ["ALERT LEVEL 2!\n", "text"],
                ["An alert level 2 has been also created <br>from the system.<br>", "html"]
            ]
            
        - Example of attaching file(s):
            # Specifying only one file
            files1 = "./testdata/bank.xlsx"
            # Specifying several files
            files2 = ["./testdata/bank.xlsx", "./testdata/OpenWeather.json"]

        - Example of sending a message:
            # Choose your message and send it
            smtp.sendMessage(
                     fromAddr = "ALERTING <data.intelligence@akka.eu>",
                     toAddrs = ["PhilAtHome <prossblad@gmail.com>", "PhilAtCompany <philippe.rossignol@akka.eu>"],
                     subject = "WARNING: System issue",
                     content = content4,
                     files = files2
            )
        '''

        # Prepare the message
        message = self.MIMEMultipart()
        message["From"] = fromAddr
        message["To"] = self.COMMASPACE.join(toAddrs)
        from email.utils import formatdate
        message["Date"] = formatdate(localtime=True)
        message["Subject"] = subject

        # Create the content (text, html or a combination)
        if (type(content) is not str and type(content) is not list): content = str(content)
        if (type(content) is str): content = [[content, "plain"]]
        for msg in content:
            if (msg[1].strip().lower() != "html"): msg[1] = "plain"
            message.attach(self.MIMEText(msg[0], msg[1]))

        # Attach the files
        if (files != None):
            if (type(files) is str): files = [files]
            for path in files:
                part = self.MIMEBase("application", "octet-stream")
                with open(path, "rb") as file: part.set_payload(file.read())
                self.encoders.encode_base64(part)
                part.add_header("Content-Disposition", 'attachment; filename="{}"'.format(self.os.path.basename(path)))
                message.attach(part)

        # Send the message
        if (fromAddr == None): fromAddr = user
        con = self.smtplib.SMTP(self.host, self.port)
        if (self.isTls): con.starttls()
        if (self.user != None and self.password != None): con.login(self.user, self.password)
        con.sendmail(fromAddr, toAddrs, message.as_string())
        con.quit()
