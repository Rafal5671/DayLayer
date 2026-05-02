import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", 1025))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@daylayer.local")

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")

jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=True,
)


def render_email(template_name: str, context: dict) -> str:
    """Render email template with context."""
    template = jinja_env.get_template(template_name)
    return template.render(**context)


async def send_email(to: str, subject: str, template: str, context: dict) -> None:
    """Render template and send email via SMTP."""
    html = render_email(template, context)

    message = MIMEMultipart("alternative")
    message["From"] = FROM_EMAIL
    message["To"] = to
    message["Subject"] = subject
    message.attach(MIMEText(html, "html"))

    try:
        smtp = aiosmtplib.SMTP(
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            use_tls=False,
            start_tls=False,
        )
        await smtp.connect()
        await smtp.sendmail(FROM_EMAIL, [to], message.as_string())
        await smtp.quit()
        print(f"Email sent to {to}: {subject}")
    except Exception as e:
        print(f"Failed to send email to {to}: {e}")
