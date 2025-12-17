import os
import logging

# Ensure 'logs' folder exists
os.makedirs('logs', exist_ok=True)

# Logging configuration
logging.basicConfig(
    filename='logs/intrusion.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

from email_alerts import send_alert_email
import datetime
import json

# Configure logging (can be adjusted as needed)
logging.basicConfig(filename='logs/intrusion.log', level=logging.WARNING, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def respond_to_intrusion(prediction):
    ip = prediction.get('ip', 'unknown')
    timestamp = datetime.datetime.now().isoformat()
    threat_type = prediction.get('attack_type', 'Unknown')

    # Log IP to blocked list
    with open('blocked_ips.txt', 'a') as f:
        f.write(f"{ip} blocked at {timestamp} for {threat_type}\n")

    # Log intrusion in JSON format
    with open('logs/alerts.json', 'a') as json_log:
        json.dump({
            'ip': ip,
            'time': timestamp,
            'threat': threat_type,
            'details': prediction
        }, json_log)
        json_log.write('\n')

    # Log to log file
    logging.warning(f"Intrusion detected and mitigated: {prediction}")

    # Send email alert
    send_alert_email(prediction)
