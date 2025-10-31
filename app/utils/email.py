from app.config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


def send_reset_email(to_email: str, token: str):
    # Simulate email sending
    # print(
    #     f"Sending reset link to {to_email}: {settings.BACKEND_URL}/auth/reset-password?token={token}"
    # )
    reset_link = f"{settings.BACKEND_URL}/auth/reset-password?token={token}"

    subject = "Password Reset Request"
    body = f"""
    <h2>Password Reset</h2>
    <p>Click the link below to reset your password:</p>
    <a href="{reset_link}">{reset_link}</a>
    <p>This link will expire in 15 minutes.</p>
    """

    msg = MIMEMultipart()
    msg["From"] = settings.EMAIL_SENDER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_SENDER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent successfully")
    except Exception as e:
        print("❌ Error sending email:", e)
        raise
