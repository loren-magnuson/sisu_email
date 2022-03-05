import unittest
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src import sisu_email


TEST_BODY_TEXT = 'test'

TEST_SENDER = 'sender123@gmail.com'

TEST_RECIPIENT = 'recipient123@gmail.com'

TEST_SUBJECT = 'test subject'

TEST_TXT_ATTACHMENT = './fixtures/test_txt_attachment.txt'


def create_test_message():
    message = sisu_email.create_multipart_message(
        TEST_SENDER,
        TEST_RECIPIENT,
        TEST_SUBJECT,
        TEST_BODY_TEXT
    )
    return message


class TestSisuEmail(unittest.TestCase):

    def test_create_multipart_message(self):
        message = create_test_message()
        self.assertIsInstance(message, MIMEMultipart)
        self.assertEqual(message['subject'], TEST_SUBJECT)
        self.assertEqual(message['From'], TEST_SENDER)
        self.assertEqual(message['To'], TEST_RECIPIENT)
        self.assertIsInstance(message.get_payload(0), MIMEText)

    def test_attach_file_to_multipart_message(self):
        message = create_test_message()


if __name__ == '__main__':
    unittest.main()
