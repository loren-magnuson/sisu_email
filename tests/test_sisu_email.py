import unittest
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src import sisu_email


class TestSisuEmail(unittest.TestCase):

    def test_create_multipart_message(self):
        body_text = 'test'
        sender = 'sender123@gmail.com'
        recipient = 'recipient123@gmail.com'
        subject = 'test subject'
        message = sisu_email.create_multipart_message(
            sender,
            recipient,
            subject,
            body_text
        )

        self.assertIsInstance(message, MIMEMultipart)
        self.assertEqual(message['subject'], subject)
        self.assertEqual(message['From'], sender)
        self.assertEqual(message['To'], recipient)
        self.assertIsInstance(message.get_payload(0), MIMEText)


if __name__ == '__main__':
    unittest.main()
