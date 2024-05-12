import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from secrets import Secrets
from attachment import Attachment  # Assuming attachment class is defined in attachment.py
# Define email body

class EmailSender:
    def __init__(self, receiver_name, receiver_email, attachment_path=None):
        self.sender_email = Secrets().get_email()
        self.sender_password = Secrets().get_pwd()
        self.receiver_name = receiver_name
        self.receiver_email = receiver_email
        self.attachment_path = attachment_path
        self.attachment_name = attachment_path.split("/")[-1]
        self.event_name = "Azure Fundamentals Workshop"
        self.event_date = "1st May 2024"
        self.email_subject = "Azure Fundamentals Workshop Completion Certificate"
    
    def send_email(self):
        subject = self.email_subject
        
        # Read the email template HTML content
        with open("email_template.html", "r") as file:
            email_body = file.read()
        
        # Replace placeholders with actual values
        email_body = email_body.replace('receiver_name', self.receiver_name)
        email_body = email_body.replace('event_name', self.event_name)
        email_body = email_body.replace('event_date', self.event_date)
        
        # Remove newline characters if needed
        email_body = email_body.replace("\n", "")

        # Create MIMEText object for HTML content
        body = MIMEText(email_body, "html")
            
        # Create MIMEMultipart message
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        message["Subject"] = subject
        
        # Attach HTML content to the email message
        message.attach(body)

        # Attach the attachment if specified
        if self.attachment_path:
            with open(self.attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={self.attachment_name}"
            )
            message.attach(part)

        # Send the email
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, self.receiver_email, message.as_string())
class Recipient:
    def __init__(self):
        self.email_lists = Attachment().get_email_list()

    def send_email(self):
        for name, email, path in self.email_lists:
            try:
                EmailSender(name, email, path).send_email()
                print(f"Email sent to {name} at {email}")
            # Handle exceptions
            except Exception as e:
                print(f"Failed to send email to {name} at {email}. Error: {e}")
                
        
def main():
    Recipient().send_email()

if __name__ == "__main__":
    main()
