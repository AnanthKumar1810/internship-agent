import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from . import config


def _build_html(listings):
    rows = ""
    for l in listings:
        rows += f"""
        <tr>
          <td style="padding:8px;border-bottom:1px solid #eee;">
            <a href="{l['link']}" style="color:#0a66c2;text-decoration:none;font-weight:600;">
              {l['title']}
            </a><br/>
            <span style="color:#555;">{l['company']} — {l['location']}</span><br/>
            <span style="color:#888;font-size:12px;">{l['source']}</span>
          </td>
        </tr>
        """
    return f"""
    <html><body style="font-family:sans-serif;">
      <h2>{len(listings)} new internship(s) found</h2>
      <table style="width:100%;border-collapse:collapse;">{rows}</table>
    </body></html>
    """


def send_email(listings):
    if not listings:
        print("No new listings — skipping email.")
        return

    if not (config.SMTP_USER and config.SMTP_PASS and config.EMAIL_TO):
        print("SMTP credentials/recipient not set — skipping email send. "
              "Set SMTP_USER, SMTP_PASS, EMAIL_TO as GitHub Actions secrets.")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"{len(listings)} new internships (AI/ML/IoT/CV)"
    msg["From"] = config.SMTP_USER
    msg["To"] = config.EMAIL_TO
    msg.attach(MIMEText(_build_html(listings), "html"))

    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
        server.starttls()
        server.login(config.SMTP_USER, config.SMTP_PASS)
        server.sendmail(config.SMTP_USER, [config.EMAIL_TO], msg.as_string())

    print(f"Sent email with {len(listings)} new listings.")
