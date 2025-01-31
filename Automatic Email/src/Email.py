import os

class Email(object):
    """
    This class models an Email to avoid dealing with the Win32 Email interface
    """
    
    def _init_(self, mail):
        self._email = mail

    def get_sender_name(self):
        return self._email.SenderName

    def get_sender_address(self):
        return self._email.Sender.Address

    def get_to_name(self):
        return self._email.To

    def get_subject(self):
        return self._email.Subject

    def get_body(self):
        return self._email.body

    def get_html_body(self):
        return self._email.HTMLBody

    def get_timestamp(self):
        return self._email.SentOn

    def save_attachments(self, path):
        """
        Saves all the attachments from the email to the specified path.
        """
        for attachment in self._email.Attachments:
            attachment.SaveAsFile(os.path.join(path, attachment.FileName))
    
    def get_attachments(self, temp_path):
        """
        Get byte content of attachments, using a temporary path to save the files and then read them
        """
        contents = []
        for a in self._email.Attachments:
            filename = os.path.join(temp_path, a.FileName)
            a.SaveAsFile(filename)
            with open(filename, 'rb') as f:
                contents.append(f.read())
    
        return contents
    
    def _str_(self):
        sender = self._email.SenderName
        to = self._email.To
        subj = self._email.Subject
        when = self._email.SentOn
        desc = f"From: {sender}, To: {to} Subject: {subj}, on: {when}"
        return desc