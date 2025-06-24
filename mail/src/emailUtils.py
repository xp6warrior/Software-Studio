import base64
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from .emailTemplates import get_email_template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

#❗❗❗❗❗MAKE SURE U HAVE YOUR OWN TOKENS.JSON AS ITS DEVICE-SPECIFIC❗❗❗❗❗
#if not then try running it without tokens then u should get a link and log in with the mail and passw stored in .env
# - that should create tokens.json for ur device and once u have it itll keep running completly automatically without any log-ins
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
TOKEN_PATH = os.path.join(os.path.dirname(__file__), "token.json")
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "credentials.json")

def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    from googleapiclient.discovery import build
    return build("gmail", "v1", credentials=creds)


def build_html_email(subject, body_text):
    logo_url = "https://raw.githubusercontent.com/xp6warrior/Software-Studio/Assets-photos/webapp/assets/Logovertical.png"
    background_gradient = "linear-gradient(90deg, #8c4fe6 0%, #3e4bf1 100%)"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>{subject}</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; background: {background_gradient};">
      <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
          <td align="center">
            <table border="0" cellpadding="0" cellspacing="0" width="600" style="background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);">
              
              <!-- Header with logo -->
              <tr>
                <td align="center" style="background: {background_gradient}; padding: 24px;">
                  <img src="{logo_url}" width="200" alt="Back2U Logo" style="display: block;" />
                </td>
              </tr>

              <!-- Email content -->
              <tr>
                <td style="padding: 30px 40px; color: #333;">
                  <h2 style="margin-top: 0; color: #333;">{subject}</h2>
                  <p style="line-height: 1.6; white-space: pre-line;">{body_text}</p>
                  
                  <hr style="border: 0; border-top: 1px solid #ddd; margin: 40px 0;">

                  <p style="margin: 0;">Best regards,<br><strong>Back2U Team</strong></p>
                </td>
              </tr>

              <!-- Footer -->
              <tr>
                <td style="padding: 15px 40px; font-size: 12px; color: #999; text-align: center;">
                  You received this email because you're registered using this address with Back2U.<br>
                  If you did not create this account or believe this was a mistake, please contact us at <a href="mailto:back2u.customerservice@gmail.com">back2u.customerservice@gmail.com</a>.
                  <br><br>
                  <span style="color: #bbb;">This email was generated automatically. Please do not reply.</span><br><br>
                  <span style="color: #bbb;">© Back2U. All rights reserved.</span>

                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """
    return html

def send_email(service, sender, to, subject, body_text):
    html_body = build_html_email(subject, body_text)

    msg = MIMEMultipart('alternative')
    msg['to'] = to
    msg['from'] = sender
    msg['subject'] = subject

    msg.attach(MIMEText(body_text, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    body = {'raw': raw}

    message = service.users().messages().send(userId='me', body=body).execute()
    print(f'Email sent! Message ID: {message["id"]}')
