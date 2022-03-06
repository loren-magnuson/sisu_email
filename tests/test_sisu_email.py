import base64
import tempfile
import unittest
import xlrd
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src import sisu_email


TEST_BODY_TEXT = 'test'

TEST_SENDER = 'sender123@gmail.com'

TEST_RECIPIENT = 'recipient123@gmail.com'

TEST_SUBJECT = 'test subject'

TEST_TXT_ATTACHMENT = './fixtures/test_txt_attachment.txt'

TEST_EXCEL_ATTACHMENT = './fixtures/test_excel_attachment.xls'


def create_test_multipart_message():
    message = sisu_email.create_multipart_message(
        TEST_SENDER,
        TEST_RECIPIENT,
        TEST_SUBJECT,
        TEST_BODY_TEXT
    )
    return message


class TestSisuEmail(unittest.TestCase):

    def test_create_multipart_message(self):
        message = create_test_multipart_message()
        self.assertIsInstance(message, MIMEMultipart)
        self.assertEqual(message['subject'], TEST_SUBJECT)
        self.assertEqual(message['From'], TEST_SENDER)
        self.assertEqual(message['To'], TEST_RECIPIENT)
        self.assertIsInstance(message.get_payload(0), MIMEText)

    def test_attach_file_to_multipart_message_text(self):
        message = create_test_multipart_message()
        with open(TEST_TXT_ATTACHMENT, 'rb') as test_txt_file:
            message = sisu_email.attach_file_to_multipart_message(
                test_txt_file,
                message
            )

            self.assertIsInstance(message.get_payload(1), MIMEBase)
            self.assertEqual(
                message.get_payload(1).get('Content-Decomposition'),
                'attachment; filename="./fixtures/test_txt_attachment.txt"'
            )

            encoded_body = message.get_payload(1).as_string().split('\n')[-2]
            self.assertEqual(
                base64.b64decode(encoded_body),
                b'this is a test text file attachment'
            )

    def test_attach_file_to_multipart_message_excel(self):
        message = create_test_multipart_message()
        with open(TEST_EXCEL_ATTACHMENT, 'rb') as test_excel_file:
            message = sisu_email.attach_file_to_multipart_message(
                test_excel_file,
                message
            )

            self.assertIsInstance(message.get_payload(1), MIMEBase)
            self.assertEqual(
                message.get_payload(1).get('Content-Decomposition'),
                'attachment; filename="./fixtures/test_excel_attachment.xls"'
            )

            encoded_body = ''.join(message.get_payload(1).as_string().split('\n')[5:-1])
            decoded_body = base64.b64decode(encoded_body)

            with tempfile.NamedTemporaryFile('wb') as outfile:
                outfile.write(decoded_body)
                outfile.seek(0)
                wb = xlrd.open_workbook(outfile.name)
                wb.sheet_by_index(0)
                self.assertEqual(
                    'TestHeader',
                    wb.sheet_by_index(0).cell(0, 0).value
                )


if __name__ == '__main__':
    unittest.main()
