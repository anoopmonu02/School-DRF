from django.core.mail import EmailMessage
import os

class Util:
    @staticmethod
    def send_email(data):
        print("Data: ", data)
        subjectMsg = data['subject']
        fromEmail = os.environ.get('EMAIL_FROM')
        bodyMsg = data['body']
        toEmails = data['to']
        print("Sending email to: ", toEmails)
        email = EmailMessage(
            subject = subjectMsg,
            body = bodyMsg,
            from_email = fromEmail,
            to=toEmails
        )
        email.send()
    
def send_normal_email(data):
    fromEmail = os.environ.get('EMAIL_FROM')
    email = EmailMessage(
            subject = data['email_subject'],
            body = data['email_body'],
            from_email = fromEmail,
            to=[data['to_email']]
        )
    email.send()