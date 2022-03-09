import base64
import tempfile
import unittest
import PyPDF2
import xlrd
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.sisu_email import create


TEST_BODY_TEXT = 'test'

TEST_SENDER = 'sender123@gmail.com'

TEST_RECIPIENT = 'recipient123@gmail.com'

TEST_SUBJECT = 'test subject'

TEST_TXT = './fixtures/test_txt.txt'

TEST_EXCEL = './fixtures/test_xls.xls'

TEST_PDF = './fixtures/test_pdf.pdf'

TEST_IMAGE = './fixtures/test_image.jpg'


def create_test_multipart_message():
    message = create.create_multipart_message(
        TEST_SENDER,
        TEST_RECIPIENT,
        TEST_SUBJECT,
        TEST_BODY_TEXT
    )
    return message


class TestCreate(unittest.TestCase):

    def test_create_multipart_message(self):
        message = create_test_multipart_message()
        self.assertIsInstance(message, MIMEMultipart)
        self.assertEqual(message['subject'], TEST_SUBJECT)
        self.assertEqual(message['From'], TEST_SENDER)
        self.assertEqual(message['To'], TEST_RECIPIENT)
        self.assertIsInstance(message.get_payload(0), MIMEText)

    def test_attach_file_text(self):
        message = create_test_multipart_message()
        with open(TEST_TXT, 'rb') as test_file:
            message = create.attach_file(test_file, message)

            self.assertIsInstance(message.get_payload(1), MIMEBase)
            self.assertEqual(
                message.get_payload(1).get('Content-Decomposition'),
                'attachment; filename="./fixtures/test_txt.txt"'
            )

            encoded_body = message.get_payload(1).as_string().split('\n')[-2]
            self.assertEqual(
                base64.b64decode(encoded_body),
                b'this is a test text file attachment'
            )

    def test_attach_file_xls(self):
        message = create_test_multipart_message()
        with open(TEST_EXCEL, 'rb') as test_file:
            message = create.attach_file(test_file, message)

            self.assertIsInstance(message.get_payload(1), MIMEBase)
            self.assertEqual(
                message.get_payload(1).get('Content-Decomposition'),
                'attachment; filename="./fixtures/test_xls.xls"'
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

    def test_attach_file_pdf(self):
        message = create_test_multipart_message()
        with open(TEST_PDF, 'rb') as test_file:
            message = create.attach_file(test_file, message)

            self.assertIsInstance(message.get_payload(1), MIMEBase)
            self.assertEqual(
                message.get_payload(1).get('Content-Decomposition'),
                'attachment; filename="./fixtures/test_pdf.pdf"'
            )

            encoded_body = ''.join(message.get_payload(1).as_string().split('\n')[5:-1])
            decoded_body = base64.b64decode(encoded_body)

            with tempfile.NamedTemporaryFile('wb') as outfile:
                outfile.write(decoded_body)
                outfile.seek(0)
                pdf_file_obj = open(outfile.name, 'rb')
                pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
                self.assertEqual(2, pdf_reader.numPages)
                page_obj = pdf_reader.getPage(0)
                first_page_text = page_obj.extractText()
                self.assertTrue(first_page_text.startswith('Lorem Ipsum'))
                self.assertTrue(first_page_text.strip().endswith('the Internet. It uses a'))
                pdf_file_obj.close()

    def test_attach_file_image(self):
        message = create_test_multipart_message()
        with open(TEST_IMAGE, 'rb') as test_file:
            message = create.attach_file(test_file, message)

            self.assertIsInstance(message.get_payload(1), MIMEBase)
            self.assertEqual(
                message.get_payload(1).get('Content-Decomposition'),
                'attachment; filename="./fixtures/test_image.jpg"'
            )

            encoded_body = ''.join(message.get_payload(1).as_string().split('\n')[5:-1])
            decoded_body = base64.b64decode(encoded_body)

            with tempfile.NamedTemporaryFile('wb') as outfile:
                outfile.write(decoded_body)
                outfile.seek(0)

                test_file.seek(0)
                with open(outfile.name, 'rb') as infile:
                    data = infile.read()
                    test_data = test_file.read()
                    self.assertEqual(data, test_data)

    def test_encode_multipart_message(self):
        """Encode multipart message as urlsafe base64 string

        :return: dict, {'raw': base64_string_of_message}
        """
        message = create_test_multipart_message()
        text_repr = str(message)
        encoded = create.encode_multipart_message(message)
        self.assertIs(str, type(encoded))
        self.assertEqual(
            text_repr,
            base64.urlsafe_b64decode(encoded).decode()
        )


if __name__ == '__main__':
    unittest.main()
