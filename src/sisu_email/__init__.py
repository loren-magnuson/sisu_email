from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def create_multipart_message(sender, recipient, subject, body_text, text_format='plain'):
    """Create multipart message with text body and text format set

    :param sender: (str) sender email address
    :param recipient: (str) recipient email address
    :param subject: (str) subject line for email
    :param body_text: (str) body text of email
    :param text_format: optional, (str) 'plain' or 'html'
    :return: email.mime.multipart.MIMEMultipart
    """
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(body_text, text_format))
    return message
