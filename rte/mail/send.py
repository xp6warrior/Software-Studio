from .emailUtils import get_gmail_service, send_email
from .emailTemplates import get_email_template

SENDER_EMAIL = "noreplyback2uapp@gmail.com"

def send_templated_email(to, template_id, name, surname, item_id=None, item_type=None):
    full_name = f"{name} {surname}"
    subject, body = get_email_template(template_id, full_name, item_id, item_type)

    print(f"Sending email to {to} with subject: {subject}")
    service = get_gmail_service()
    send_email(service, SENDER_EMAIL, to, subject, body)

#THIS IS THE FORM IN WHICH WE CAN USE THE SENDING FUNCTION
#send_templated_email(
#    to="back2u.user@gmail.com",
#    template_id=3,
#    name="X",
#    surname="Y",
#    item_id=123,
#    item_type="Clothing"
#)
