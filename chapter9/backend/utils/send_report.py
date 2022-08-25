# send report by email
from decouple import config

import sendgrid
from sendgrid.helpers.mail import *

SENDGRID_ID = config("SENDGRID_ID", cast=str)


def send_report(email, subject, HTMLcontent):

    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_ID)
    from_email = Email("FARM@freethrow.rs")
    to_email = To(email)
    subject = "FARM Cars daily report"
    content = Content(
        "text/plain", "this is dynamic text, potentially coming from our database"
    )

    mail = Mail(from_email, to_email, subject, content, html_content=HTMLcontent)

    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response)
        print("Sending email")
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
        print(e)
        print("Could not send email")
