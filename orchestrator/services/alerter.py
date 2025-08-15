import logging
import smtplib
import time
from email.mime.text import MIMEText
from typing import Dict, Any
from services.db.db_methods import update_host_status
from config import NEXT_EMAIL_DELAY

class Alerter:
    def __init__(self, smtp_server: str, smtp_port: int, smtp_user: str, smtp_pass: str, recipient_email: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass
        self.recipient_email = recipient_email
        self.logger = self.conf_alerter_logger()
        self.last_alert_time = 0

    def conf_alerter_logger(self):
        logger = logging.getLogger('alerter')
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler("logs/alerter.log")
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    def check_and_alert(self, profile: Dict[str, Any], metrics: Dict[str, Any]) -> str:
        host_name = profile['name']
        status_id = profile['status_id']
        current_state = profile['state']

        cpu_ok = metrics['cpu_percent'] <= profile['cpu_percentage']
        mem_ok = metrics['mem_percent'] <= profile['mem_percentage']
        disk_ok = metrics['disk_percent'] <= profile['disk_percentage']
        
        if not cpu_ok or not mem_ok or not disk_ok:
            # Threshold exceeded, change status to 'WARNING' if not already there
            if current_state != 'WARNING':
                update_host_status(status_id, "WARNING", None)
                message = f"""
                    ALERT: Resource threshold exceeded for host '{host_name}'.\n\n
                    CPU Usage: {metrics['cpu_percent']}% (Threshold: {profile['cpu_percentage']}%) \n
                    Memory Usage: {metrics['mem_percent']}% (Threshold: {profile['mem_percentage']}%) \n
                    Disk Usage: {metrics['disk_persent']}% (Threshold: {profile['disk_percentage']}%) \n
                """
                self.logger.warning(f"Threshold exceeded for {host_name}. Sending alert.")
                if(time.time() - self.last_alert_time > NEXT_EMAIL_DELAY):
                    try:
                        self._send_email_alert("Resource Alert", message)
                        self.last_alert_time = time.time()
                    except EmailSendingError as e:
                        self.logger.error(f"Failed to send email alert: {e}")
            return "WARNING"
        else:
            # All metrics are within thresholds, change status to 'UP' if not already there
            if current_state != 'UP':
                update_host_status(status_id, "UP", None)
                self.logger.info(f"Host {host_name} is back within normal thresholds. Status changed to UP.")
            return "UP"

    def _send_email_alert(self, subject: str, body: str):
        """
        Sends an email alert to the configured recipient.
        """
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.smtp_user
            msg['To'] = self.recipient_email

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.sendmail(self.smtp_user, self.recipient_email, msg.as_string())
            self.logger.info(f"Successfully sent email alert to {self.recipient_email}")
        except Exception as e:
            raise EmailSendingError(f"SMTP error: {e}")

class EmailSendingError(Exception):
    pass
