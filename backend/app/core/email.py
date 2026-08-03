"""Email delivery: SMTP in production, console fallback in dev/test."""
import logging
import smtplib
from email.message import EmailMessage
from email.utils import formataddr

from app.core.config import Settings

logger = logging.getLogger("carecode.email")


def _build_message(settings: Settings, to: str, subject: str, html: str) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr((settings.smtp_from_name, settings.smtp_from_email))
    msg["To"] = to
    msg.set_content("This email requires an HTML-capable client.")
    msg.add_alternative(html, subtype="html")
    return msg


def send_email(settings: Settings, to: str, subject: str, html: str) -> bool:
    """Send via SMTP. Falls back to logging the message (dev/test). Returns True on success."""
    if not settings.smtp_configured:
        logger.warning("[console-email] To=%s Subject=%s\n%s", to, subject, html)
        return True

    msg = _build_message(settings, to, subject, html)
    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as server:
            if settings.smtp_use_tls:
                server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(msg)
        logger.info("Email sent to %s", to)
        return True
    except Exception:
        logger.exception("Failed to send email to %s", to)
        return False


# --------------------------------------------------------------------------
# Templates
# --------------------------------------------------------------------------
def password_reset_email(settings: Settings, to: str, reset_url: str) -> bool:
    subject = "CareCode — Reset your password"
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <body style="margin:0;padding:0;background:#f1f5f9;font-family:Arial,Helvetica,sans-serif;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f1f5f9;padding:24px 0;">
        <tr><td align="center">
          <table role="presentation" width="100%" style="max-width:480px;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(2,6,23,.08);">
            <tr>
              <td style="background:#0B5FFF;padding:24px 32px;">
                <span style="color:#ffffff;font-size:22px;font-weight:bold;">&#9671; CareCode</span>
                <span style="color:#bfdbfe;font-size:22px;font-weight:bold;"> · Scan. Care. Save Lives.</span>
              </td>
            </tr>
            <tr>
              <td style="padding:32px;">
                <h1 style="margin:0 0 12px;font-size:20px;color:#0f172a;">Reset your password</h1>
                <p style="margin:0 0 20px;font-size:14px;line-height:1.6;color:#475569;">
                  We received a request to reset the password for your CareCode account
                  (<strong>{to}</strong>). This link is valid for
                  <strong>{settings.reset_token_expire_minutes} minutes</strong> and can be used once.
                </p>
                <p style="margin:0 0 24px;font-size:14px;line-height:1.6;color:#475569;">
                  If you did not request this, you can safely ignore this email.
                </p>
                <table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 24px;">
                  <tr>
                    <td style="border-radius:10px;background:#0B5FFF;">
                      <a href="{reset_url}" style="display:inline-block;padding:14px 32px;color:#ffffff;text-decoration:none;font-size:15px;font-weight:bold;">Reset Password</a>
                    </td>
                  </tr>
                </table>
                <p style="margin:0;font-size:12px;color:#94a3b8;">
                  If the button does not work, copy and paste this link into your browser:<br/>
                  <span style="word-break:break-all;color:#0B5FFF;">{reset_url}</span>
                </p>
              </td>
            </tr>
            <tr>
              <td style="background:#f8fafc;padding:16px 32px;font-size:12px;color:#94a3b8;">
                CareCode · Emergency medical identification
              </td>
            </tr>
          </table>
        </td></tr>
      </table>
    </body>
    </html>
    """
    return send_email(settings, to, subject, html)
