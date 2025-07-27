import json
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MonitoringAlert:
    def __init__(self, config_path: str = "config/monitoring.json"):
        """Initialize the monitoring alert system with configuration."""
        self.config = self._load_config(config_path)
        self.alert_history: List[Dict] = []

    def _load_config(self, config_path: str) -> Dict:
        """Load monitoring configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load monitoring config: {e}")
            return {}

    def check_thresholds(self, metrics: Dict) -> List[Dict]:
        """Check if any metrics exceed configured thresholds."""
        alerts = []
        thresholds = self.config.get('alerts', {})

        # Check CPU usage
        if 'cpu' in metrics and 'usage' in metrics['cpu']:
            cpu_usage = metrics['cpu']['usage']
            if cpu_usage >= thresholds.get('cpu', {}).get('critical', 90):
                alerts.append({
                    'type': 'critical',
                    'metric': 'cpu',
                    'value': cpu_usage,
                    'threshold': thresholds['cpu']['critical'],
                    'timestamp': datetime.utcnow().isoformat()
                })
            elif cpu_usage >= thresholds.get('cpu', {}).get('warning', 70):
                alerts.append({
                    'type': 'warning',
                    'metric': 'cpu',
                    'value': cpu_usage,
                    'threshold': thresholds['cpu']['warning'],
                    'timestamp': datetime.utcnow().isoformat()
                })

        # Check memory usage
        if 'memory' in metrics and 'usage_percent' in metrics['memory']:
            mem_usage = metrics['memory']['usage_percent']
            if mem_usage >= thresholds.get('memory', {}).get('critical', 90):
                alerts.append({
                    'type': 'critical',
                    'metric': 'memory',
                    'value': mem_usage,
                    'threshold': thresholds['memory']['critical'],
                    'timestamp': datetime.utcnow().isoformat()
                })
            elif mem_usage >= thresholds.get('memory', {}).get('warning', 75):
                alerts.append({
                    'type': 'warning',
                    'metric': 'memory',
                    'value': mem_usage,
                    'threshold': thresholds['memory']['warning'],
                    'timestamp': datetime.utcnow().isoformat()
                })

        # Check disk usage
        if 'disk' in metrics and 'usage_percent' in metrics['disk']:
            disk_usage = metrics['disk']['usage_percent']
            if disk_usage >= thresholds.get('disk', {}).get('critical', 95):
                alerts.append({
                    'type': 'critical',
                    'metric': 'disk',
                    'value': disk_usage,
                    'threshold': thresholds['disk']['critical'],
                    'timestamp': datetime.utcnow().isoformat()
                })
            elif disk_usage >= thresholds.get('disk', {}).get('warning', 80):
                alerts.append({
                    'type': 'warning',
                    'metric': 'disk',
                    'value': disk_usage,
                    'threshold': thresholds['disk']['warning'],
                    'timestamp': datetime.utcnow().isoformat()
                })

        return alerts

    def send_email_alert(self, alert: Dict) -> bool:
        """Send email alert for critical issues."""
        if not self.config.get('notifications', {}).get('email', {}).get('enabled', False):
            return False

        email_config = self.config['notifications']['email']
        try:
            msg = MIMEMultipart()
            msg['From'] = f"Daena Monitoring <{email_config['smtp_server']}>"
            msg['To'] = ", ".join(email_config['recipients'])
            msg['Subject'] = f"Daena Alert: {alert['type'].upper()} - {alert['metric']}"

            body = f"""
            Alert Type: {alert['type'].upper()}
            Metric: {alert['metric']}
            Current Value: {alert['value']}%
            Threshold: {alert['threshold']}%
            Timestamp: {alert['timestamp']}
            """

            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(email_config['smtp_server'], email_config['port']) as server:
                server.starttls()
                server.send_message(msg)

            logger.info(f"Email alert sent for {alert['metric']}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            return False

    def send_webhook_alert(self, alert: Dict) -> bool:
        """Send webhook alert for critical issues."""
        if not self.config.get('notifications', {}).get('webhook', {}).get('enabled', False):
            return False

        webhook_config = self.config['notifications']['webhook']
        try:
            headers = {
                'Content-Type': 'application/json',
                'X-Webhook-Secret': webhook_config['secret']
            }
            
            response = requests.post(
                webhook_config['url'],
                json=alert,
                headers=headers
            )
            
            if response.status_code == 200:
                logger.info(f"Webhook alert sent for {alert['metric']}")
                return True
            else:
                logger.error(f"Webhook alert failed with status {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Failed to send webhook alert: {e}")
            return False

    def process_alerts(self, metrics: Dict) -> None:
        """Process metrics and send alerts if necessary."""
        alerts = self.check_thresholds(metrics)
        
        for alert in alerts:
            self.alert_history.append(alert)
            
            # Send notifications for critical alerts
            if alert['type'] == 'critical':
                self.send_email_alert(alert)
                self.send_webhook_alert(alert)
            
            # Log all alerts
            logger.warning(
                f"{alert['type'].upper()} Alert: {alert['metric']} at {alert['value']}% "
                f"(threshold: {alert['threshold']}%)"
            )

    def get_alert_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get alert history, optionally limited to the most recent alerts."""
        if limit is None:
            return self.alert_history
        return self.alert_history[-limit:]

    def clear_alert_history(self) -> None:
        """Clear the alert history."""
        self.alert_history = [] 