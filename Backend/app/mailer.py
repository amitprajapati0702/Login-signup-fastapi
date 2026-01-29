from app.config import HOST, USERNAME, PASSWORD, PORT
from ssl import create_default_context
from app.Schema import MailBody
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP

def send_email(data: dict) -> bool:
    try:
        msg = MailBody(**data)

        message = MIMEMultipart("alternative")
        message["From"] = USERNAME # pyright: ignore[reportArgumentType]
        message["To"] = ", ".join(msg.to)
        message["Subject"] = msg.subject

        html_body = MIMEText(msg.body, "html")
        message.attach(html_body)

        context = create_default_context()

        with SMTP(HOST, PORT) as server: # pyright: ignore[reportArgumentType]
            server.starttls(context=context)
            server.login(USERNAME, PASSWORD) # pyright: ignore[reportArgumentType]
            server.sendmail(
                USERNAME, # pyright: ignore[reportArgumentType]
                msg.to,
                message.as_string()
            )

        return True

    except Exception as e:
        print("Email sending failed:", e)
        return False