import win32com.client as win32
import Email

class Email_Access(object):
    """
    This class encapsulates email (Outlook) functionality so that we can send and read emails,
    being able to access the personal folders, retrieve emails based on filters.
    """

    _outlook = win32.Dispatch("Outlook.Application")
    _mapi = _outlook.GetNamespace("MAPI")

    def _init_(self):
        """
        Access to outlook application
        """
        self._outlook = win32.Dispatch("Outlook.Application")
        self._mapi = self._outlook.GetNamespace("MAPI")

    @staticmethod
    def read_msg(path):
        """
        Read an email
        """
        mapi = Email_Access._outlook.GetNamespace("MAPI")
        msg = Email_Access._mapi.OpenSharedItem(path)
        email = Email.Email(msg)
    
        del mapi
    
        return email

    def send_email(self, 
                   to_address, 
                   subject, 
                   body,
                   attachment_paths=[],
                   html_body=False,
                   cc_address=None,
                   sensitivity=3):
        """
        Send an email.
        Arguments:
        to_address: str, address to include in the email
        subject: subject text
        body: body text, plain text. If HTML is required, use HTMLBody attribute
        attachment_paths: List of str with the path of the attached files
        cc_address: str, addresses to include in the cc
        sensitivity: 3 (Confidential), 0 (Normal), 1 (Personal), 2 (Private)
        Returns: None, sends an email
        """
        mail = Email_Access._outlook.CreateItem(0)

        # Add addresses
        mail.To = to_address
        if cc_address is not None:
            mail.CC = cc_address

        # Set subject and body
        mail.Subject = subject
        if html_body:
            mail.HTMLBody = body
        else:
            mail.Body = body

        # Attach files if provided
        for attachment in attachment_paths:
            mail.Attachments.Add(attachment)

        # Set sensitivity
        mail.Sensitivity = sensitivity

        # Send email
        mail.Send()

def get_personal_folder(self, folder_path):
    """
    Get a reference to a folder located in the 'Personal Folders' section of your inbox.
    Arguments:
    - folder_path: Path to the folder we want to access, separated by '.'
    Returns:
    - Object pointer to a given mail box personal folder
    """
    route = folder_path.split(":")
    
    # Access to first level
    personal_folder = Email_Access._mapi.Folders.Item("Personal Folders")
    folder = personal_folder.Folders(route[0])

    # For each additional level in the path tree, go to the next level
    for level in route[1:]:
        folder = folder.Folders(level)

    return folder

def get_cloud_folder(self, username, folder_path):
    """
    Get a reference to a folder located in the main section of your inbox.
    Arguments:
    - username: username
    - folder_path: Path to the folder we want to access, separated by '.'
    Returns:
    - Object pointer to a given mail box personal folder
    """
    route = folder_path.split(":")
    
    # Access to personal folder
    personal_folder = Email_Access._mapi.Folders.Item(username)
    folder = personal_folder.Folders(route[0])

    # For each additional level in the path tree, go to the next level
    for level in route[1:]:
        folder = folder.Folders(level)

    return folder

def get_mails_after_date(self, folder, day_stamp):
    """
    Get an iterator to mails in the folder after a given time stamp.
    
    Arguments:
    - folder: object pointer to a mail box folder
    - day_stamp: datetime with the cut date so that we get mails after this day
    
    Returns:
    - Iterator to mails after the time stamp
    """
    sFilter = "[SentOn] > '{}-{:02d}-{:02d} 00:00 AM'".format(day_stamp.year, day_stamp.month, day_stamp.day)

    filteredEmails = folder.Items.Restrict(sFilter)

    # Return as a list of email objects
    emails = []
    for mail in filteredEmails:
        emails.append(Email.Email(mail))

    return emails

def get_mails_between_date(self, folder, from_stamp, to_stamp):
    """
    Get an iterator to mails in the folder after a given time stamp.
    
    Arguments:
    - folder: object pointer to a mail box folder
    - from_stamp: datetime with the cut date so that we get mails after this day
    - to_stamp: datetime with the cut date so that we get mails before this day
    
    Returns:
    - Iterator to mails after the time stamp
    """
    sFilter = "[SentOn] >= '{}-{:02d}-{:02d} 00:00 AM'".format(from_stamp.year, from_stamp.month, from_stamp.day)
    sFilter += " AND [SentOn] <= '{}-{:02d}-{:02d} 00:00 AM'".format(to_stamp.year, to_stamp.month, to_stamp.day)

    filteredEmails = folder.Items.Restrict(sFilter)

    # Return as a list of email objects
    emails = []
    for mail in filteredEmails:
        emails.append(Email.Email(mail))

    return emails

# if _name_ == "_main_":

# outlook = Email_Access()

# # Test sending an email
# outlook.send_email('juannrodriguezpeinado@gruposantander.com',
#                    'This is a test',
#                    'This is a test', 
#                    html_body=True)

# Access to personal folder for broker prices and get today's emails
# folder = outlook.get_personal_folder('Broker Prices: Correlation')
# folder = outlook.get_cloud_folder('juan.al.rodriguez@gruposantander.com', 'Bandeja de entrada')

# today_mails = outlook.get_mails_after_date(folder, dt.datetime(2021, 8, 3))

# # Read mails of today
# for mail in today_mails:
#     print(mail)

# # Get mails between two dates
# month_mails = outlook.get_mails_between_date(folder, 
#                                              dt.datetime(2021, 8, 23), 
#                                              dt.datetime(2021, 8, 24))

# for mail in month_mails:
#     print(mail)