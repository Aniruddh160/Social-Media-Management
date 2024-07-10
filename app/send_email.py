# app/email_utils.py

import os
import smtplib
import ssl
from email.message import EmailMessage

EMAIL_SENDER = 'textstone788@gmail.com'
EMAIL_PASSWORD = 'xumc kcda vtok ffij'

def send_login_notification(email_receiver: str):
    subject = "Log In Activity"
    body = '''
    A new Log In has been detected.
    ''' 

    em = EmailMessage()
    em['From'] = EMAIL_SENDER
    em['To'] = email_receiver  
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(em)
        print("Email sent successfully.")
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")























# import os
# import smtplib
# import ssl
# from email.message import EmailMessage


# email_sender = 'aniruddhsrinivasan160@gmail.com'
# email_password = 'gvsr ktfp xupn armk'
# email_receiver = 'aniruddh11121@gmail.com'

# subject = "Log In Activity"
# body = '''
#     A new Log In has been detected.
# '''

# em = EmailMessage()
# em['From'] = email_sender
# em['To'] = email_receiver  
# em['Subject'] = subject
# em.set_content(body)

# context = ssl.create_default_context()


# try:
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#         smtp.login(email_sender, email_password)
#         smtp.send_message(em)
#     print("Email sent successfully.")
# except smtplib.SMTPAuthenticationError as e:
#     print(f"SMTP Authentication Error: {e}")
# except Exception as e:
#     print(f"Failed to send email. Error: {e}")



# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

# def send_login_notification_email(user_email):
#     message = Mail(
#         from_email='aniruddh11121@gmail.com',  # Replace with your verified sender email
#         to_emails=user_email,
#         subject='Login Notification',
#         plain_text_content=f'Hello,\n\nYour email {user_email} has logged in to the application.'
#     )
    
#     try:
#         sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
#         response = sg.send(message)
#         print(f"Login notification email sent to {user_email}, status code: {response.status_code}")
#     except Exception as e:
#         print(f"Failed to send login notification email to {user_email}: {str(e)}")

# if __name__ == '__main__':
#     user_email = "aniruddhsrinivasan160@gmail.com"  # Replace with actual user's email
#     send_login_notification_email(user_email)
