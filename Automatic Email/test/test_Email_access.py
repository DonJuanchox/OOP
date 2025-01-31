import unittest
from unittest.mock import MagicMock, patch
import datetime
from Email_access import Email_Access

class TestEmailAccess(unittest.TestCase):

    @patch('win32com.client.Dispatch')
    def setUp(self, mock_dispatch):
        """Set up the mocks before each test"""
        self.mock_outlook = MagicMock()
        self.mock_mapi = MagicMock()

        # Patch the Dispatch to return a mock Outlook object
        mock_dispatch.return_value = self.mock_outlook
        self.mock_outlook.GetNamespace.return_value = self.mock_mapi
        
        # Initialize the Email_Access instance
        self.email_access = Email_Access()

    def test_init(self):
        """Test that Outlook and MAPI are initialized properly"""
        self.mock_outlook.GetNamespace.assert_called_with("MAPI")
        self.assertEqual(self.email_access._outlook, self.mock_outlook)
        self.assertEqual(self.email_access._mapi, self.mock_mapi)

    @patch('Email_access.Email.Email')
    def test_read_msg(self, mock_email):
        """Test the read_msg method to ensure an email is read correctly"""
        path = "some_email_path.msg"
        mock_msg = MagicMock()
        self.mock_mapi.OpenSharedItem.return_value = mock_msg
        
        email = self.email_access.read_msg(path)

        self.mock_mapi.OpenSharedItem.assert_called_once_with(path)
        mock_email.assert_called_once_with(mock_msg)
        self.assertEqual(email, mock_email(mock_msg))

    @patch('Email_access.Email.Email')
    def test_send_email(self, mock_email):
        """Test the send_email method to ensure an email is created and sent"""
        # Mock email creation
        mock_mail = MagicMock()
        self.mock_outlook.CreateItem.return_value = mock_mail

        to_address = "test@example.com"
        subject = "Test Subject"
        body = "Test Body"
        attachment_paths = ['file1.txt', 'file2.pdf']

        self.email_access.send_email(
            to_address=to_address,
            subject=subject,
            body=body,
            attachment_paths=attachment_paths,
            html_body=False,
            cc_address=None,
            sensitivity=0
        )

        # Check if the email was composed and sent properly
        self.assertEqual(mock_mail.To, to_address)
        self.assertEqual(mock_mail.Subject, subject)
        self.assertEqual(mock_mail.Body, body)
        mock_mail.Attachments.Add.assert_any_call('file1.txt')
        mock_mail.Attachments.Add.assert_any_call('file2.pdf')
        self.assertEqual(mock_mail.Sensitivity, 0)
        mock_mail.Send.assert_called_once()

    def test_get_personal_folder(self):
        """Test retrieval of personal folders"""
        folder_path = "Inbox:Subfolder"
        folder = MagicMock()

        # Mock folder access
        personal_folder = MagicMock()
        personal_folder.Folders.Item.return_value = folder
        self.mock_mapi.Folders.Item.return_value = personal_folder

        result_folder = self.email_access.get_personal_folder(folder_path)

        self.mock_mapi.Folders.Item.assert_called_once_with("Personal Folders")
        personal_folder.Folders.Item.assert_any_call("Inbox")
        folder.Folders.assert_any_call("Subfolder")
        self.assertEqual(result_folder, folder.Folders.return_value)

    def test_get_mails_after_date(self):
        """Test retrieving emails after a specific date"""
        folder = MagicMock()
        day_stamp = datetime.datetime(2023, 9, 1)
        filtered_emails = [MagicMock(), MagicMock()]
        
        # Mock folder and filtering behavior
        folder.Items.Restrict.return_value = filtered_emails

        emails = self.email_access.get_mails_after_date(folder, day_stamp)

        sFilter = "[SentOn] > '2023-09-01 00:00 AM'"
        folder.Items.Restrict.assert_called_once_with(sFilter)
        self.assertEqual(len(emails), 2)

    def test_get_mails_between_date(self):
        """Test retrieving emails between two dates"""
        folder = MagicMock()
        from_stamp = datetime.datetime(2023, 9, 1)
        to_stamp = datetime.datetime(2023, 9, 7)
        filtered_emails = [MagicMock(), MagicMock()]

        # Mock folder and filtering behavior
        folder.Items.Restrict.return_value = filtered_emails

        emails = self.email_access.get_mails_between_date(folder, from_stamp, to_stamp)

        sFilter = "[SentOn] >= '2023-09-01 00:00 AM' AND [SentOn] <= '2023-09-07 00:00 AM'"
        folder.Items.Restrict.assert_called_once_with(sFilter)
        self.assertEqual(len(emails), 2)

if __name__ == '__main__':
    unittest.main()
