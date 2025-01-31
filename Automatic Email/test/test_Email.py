import unittest
from unittest.mock import MagicMock
import os
from Email import Email

class TestEmail(unittest.TestCase):

    def setUp(self):
        """Set up a mock email object before each test"""
        self.mock_mail = MagicMock()
        self.email = Email(self.mock_mail)

    def test_get_sender_name(self):
        """Test retrieving the sender's name"""
        self.mock_mail.SenderName = "John Doe"
        sender_name = self.email.get_sender_name()
        self.assertEqual(sender_name, "John Doe")

    def test_get_sender_address(self):
        """Test retrieving the sender's email address"""
        self.mock_mail.Sender.Address = "johndoe@example.com"
        sender_address = self.email.get_sender_address()
        self.assertEqual(sender_address, "johndoe@example.com")

    def test_get_to_name(self):
        """Test retrieving the recipient's name"""
        self.mock_mail.To = "recipient@example.com"
        to_name = self.email.get_to_name()
        self.assertEqual(to_name, "recipient@example.com")

    def test_get_subject(self):
        """Test retrieving the subject of the email"""
        self.mock_mail.Subject = "Test Subject"
        subject = self.email.get_subject()
        self.assertEqual(subject, "Test Subject")

    def test_get_body(self):
        """Test retrieving the body of the email"""
        self.mock_mail.body = "This is a test body"
        body = self.email.get_body()
        self.assertEqual(body, "This is a test body")

    def test_get_html_body(self):
        """Test retrieving the HTML body of the email"""
        self.mock_mail.HTMLBody = "<p>This is a test HTML body</p>"
        html_body = self.email.get_html_body()
        self.assertEqual(html_body, "<p>This is a test HTML body</p>")

    def test_get_timestamp(self):
        """Test retrieving the timestamp of the email"""
        self.mock_mail.SentOn = "2023-09-08 10:00:00"
        timestamp = self.email.get_timestamp()
        self.assertEqual(timestamp, "2023-09-08 10:00:00")

    @unittest.mock.patch("os.path.join", side_effect=lambda *args: "/".join(args))
    def test_save_attachments(self, mock_path_join):
        """Test saving attachments to a specified path"""
        mock_attachment = MagicMock()
        mock_attachment.FileName = "test.txt"
        self.mock_mail.Attachments = [mock_attachment]

        path = "/some/path"
        self.email.save_attachments(path)

        mock_path_join.assert_called_with(path, "test.txt")
        mock_attachment.SaveAsFile.assert_called_once_with("/some/path/test.txt")

    @unittest.mock.patch("os.path.join", side_effect=lambda *args: "/".join(args))
    @unittest.mock.patch("builtins.open", unittest.mock.mock_open())
    def test_get_attachments(self, mock_path_join, mock_open):
        """Test getting the byte content of attachments"""
        mock_attachment = MagicMock()
        mock_attachment.FileName = "test.txt"
        self.mock_mail.Attachments = [mock_attachment]

        temp_path = "/temp"
        content = self.email.get_attachments(temp_path)

        mock_path_join.assert_called_with(temp_path, "test.txt")
        mock_attachment.SaveAsFile.assert_called_once_with("/temp/test.txt")
        mock_open.assert_called_with("/temp/test.txt", 'rb')
        mock_open().read.assert_called_once()
        self.assertEqual(content, [mock_open().read()])

    def test_str_representation(self):
        """Test the string representation of the email"""
        self.mock_mail.SenderName = "John Doe"
        self.mock_mail.To = "recipient@example.com"
        self.mock_mail.Subject = "Test Subject"
        self.mock_mail.SentOn = "2023-09-08 10:00:00"
        
        str_repr = str(self.email)
        expected_repr = "From: John Doe, To: recipient@example.com Subject: Test Subject, on: 2023-09-08 10:00:00"
        self.assertEqual(str_repr, expected_repr)

if __name__ == '__main__':
    unittest.main()
