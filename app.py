from flask import Flask, render_template, redirect, url_for, request, session, jsonify , flash
import pickle
import numpy as np
import random  # Added for randomization
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load AI model
with open('intrusion_model.pkl', 'rb') as f:
    intrusion_model = pickle.load(f)

# Helper functions with randomization
def get_random_attack_stats():
    return {
        'labels': ['DoS', 'SQLi', 'XSS', 'Phishing', 'Brute Force', 'Insider', 'Malware'],
        'counts': [random.randint(1, 10) for _ in range(7)]
    }

def get_random_logs(log_type):
    log_pools = {
        'email': [
            {'type': 'Phishing', 'sender': f'fake{random.randint(100,999)}@bank.com', 'status': 'Blocked', 'time': '2025-06-10 10:00'},
            {'type': 'Spoofing', 'sender': f'admin{random.randint(1,9)}@company.com', 'status': 'Blocked', 'time': '2025-06-10 11:00'}
        ],
        'brute': [
            {'username': 'admin', 'ip': f'192.168.1.{random.randint(1,50)}', 'attempts': random.randint(5,20), 'status': 'Blocked', 'time': '2025-06-10 12:00'}
        ],
        'insider': [
            {'user': f'user{random.randint(1,9)}', 'action': 'Accessed confidential data', 'status': 'Alert', 'time': '2025-06-10 13:00'}
        ],
        'app': [
            {'type': 'SQLi', 'endpoint': '/login', 'status': 'Blocked', 'time': '2025-06-10 14:00'},
            {'type': 'XSS', 'endpoint': '/profile', 'status': 'Blocked', 'time': '2025-06-10 15:00'}
        ],
        'malware': [
            {'type': 'Keylogger', 'host': f'192.168.1.{random.randint(10,99)}', 'status': 'Blocked', 'time': '2025-06-10 16:00'}
        ]
    }
    return random.sample(log_pools[log_type], k=random.randint(1, len(log_pools[log_type])))

def detect_email_threats(email_logs):
    threats = []
    for log in email_logs:
        # Detect phishing or spoofing
        if 'phishing' in log['type'].lower() or 'spoofing' in log['type'].lower():
            threats.append({
                'type': log['type'],
                'sender': log['sender'],
                'status': log['status'],
                'time': log['time'],
                'threat': 'Phishing or Spoofing detected'
            })
        # You can add more detection logic for other email threats here
    return threats

def generate_incoming_email(recipient):
    senders = [
        'fake@bank.com', 'admin@company.com', 'security@paypal.com', 'alerts@yourbank.com'
    ]
    types = ['Phishing', 'Spoofing', 'Malware', 'Normal']
    sender = random.choice(senders)
    email_type = random.choice(types)
    subject = f"Important update from {sender.split('@')[1]}"
    status = 'Blocked' if email_type in ['Phishing', 'Spoofing', 'Malware'] else 'Allowed'
    message = ""
    if status == 'Blocked':
        message = f"This email was blocked due to {email_type} threat."
    else:
        message = "This email was delivered successfully."
    return {
        'type': email_type,
        'sender': sender,
        'recipient': recipient,
        'subject': subject,
        'status': status,
        'time': f"2025-06-10 {random.randint(10,23)}:00",
        'msg': message
    }

def generate_threat_message():
    threats = [
        "Phishing attempt detected: Please verify your account.",
        "Suspicious login detected from a new device.",
        "Malware attachment blocked.",
        "Password reset request from unknown location.",
        "Spoofed email pretending to be your bank."
    ]
    return random.choice(threats)

def is_intrusion(features):
    result = intrusion_model.predict([features])
    return result[0] == -1

def extract_features_from_request(request):
    return np.random.randn(4)

def log_intrusion(event_type, features):
    print(f"Intrusion blocked: {event_type}, features: {features}")

def add_insider_threat(user, action, status, time):
    log = {
        'user': user,
        'action': action,
        'status': status,
        'time': time
    }
    if 'insider_logs' not in session:
        session['insider_logs'] = []
    session['insider_logs'].insert(0, log)  # newest first
    session.modified = True


# Authentication
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# Routes

@app.route('/send-threat-email')
@login_required
def send_threat_email():
    user_email = session.get('user_email')
    if not user_email:
        return redirect(url_for('set_email'))

    # Simulate sending email (for demo, you can print or log instead of real send)
    threat_msg = generate_threat_message()
    # For a real email, uncomment and configure the following:
    """
    msg = MIMEText(threat_msg)
    msg['Subject'] = 'Security Alert: Suspicious Email Detected'
    msg['From'] = 'noreply@yourips.com'
    msg['To'] = user_email

    # Configure your SMTP server here
    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login('your_email@example.com', 'your_password')
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
    """
    # For demo, log the sent email
    if 'email_logs' not in session:
        session['email_logs'] = []
    session['email_logs'].insert(0, {
        'type': 'Phishing',
        'sender': 'attacker@evil.com',
        'subject': 'Security Alert',
        'status': 'Blocked',
        'time': '2025-06-12 18:30',
        'msg': threat_msg,
        'recipient': user_email
    })
    session.modified = True

    flash(f"A threat email was sent to {user_email} and detected by the IPS.", "danger")
    return redirect(url_for('email_security'))

@app.route('/set-email', methods=['GET', 'POST'])
@login_required
def set_email():
    if request.method == 'POST':
        user_email = request.form['user_email']
        session['user_email'] = user_email
        return redirect(url_for('send_threat_email'))
    return render_template('set_email.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        features = extract_features_from_request(request)
        if is_intrusion(features):
            log_intrusion('login', features)
            return render_template('login.html', error="Intrusion detected and blocked!")
        
        user = request.form['username']
        pw = request.form['password']
        if user == 'tejaswini.wankhedd=e242vit.edu' and pw == 'admin':  # adjust for your demo
            session['user'] = user
            session['user_email'] = user  # <-- store email in session
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Dynamic protected routes
@app.route('/')
@login_required
def dashboard():
    attack_stats = get_random_attack_stats()
    return render_template(
        'dashboard.html',
        stats=attack_stats,
        zipped=zip(attack_stats['labels'], attack_stats['counts']),
        detected_threats=random.sample([
            "Malware detected and quarantined",
            "Brute force attempt blocked",
            "Phishing email intercepted",
            "Suspicious SQL injection attempt",
            "Unauthorized access attempt from insider"
        ], k=3)
    )

@app.route('/monitor')
@login_required
def monitor():
    attack_data = get_random_attack_stats()  # This generates new random data each time
    return render_template('monitor.html', attack_data=attack_data)

@app.route('/email-security')
@login_required
def email_security():
 # Simulate receiving a new email on each visit
    recipient = session.get('user_email', 'user@example.com')
    new_email = generate_incoming_email(recipient)

    if 'email_logs' not in session:
        session['email_logs'] = []

    session['email_logs'].insert(0, new_email)
    session.modified = True

    # Add the new email to the log (keeps all previous logs)
    session['email_logs'].insert(0, new_email)  # newest first
    session.modified = True

    return render_template('email_security.html', logs=session['email_logs'])
       


@app.route('/brute-force')
@login_required
def brute_force():
    return render_template('brute_force.html', logs=get_random_logs('brute'))

@app.route('/insider-threats')
@login_required
def insider_threats():
    # Simulate detection of a new insider threat (for demo, you can randomize or use real detection)
    new_log = {
        'user': random.choice(['tejas', 'aditi', 'arnav', 'aditya']),
        'action': random.choice(['Accessed confidential data', 'Exported sensitive file', 'Unauthorized access attempt']),
        'status': random.choice(['Alert', 'Blocked', 'Allowed']),
        'time': f"2025-06-10 {random.randint(10, 23)}:{random.choice(['00', '15', '30', '45'])}"
    }

    # Initialize history if not present
    if 'insider_logs' not in session:
        session['insider_logs'] = []

    # Add the new log to the top of the list
    session['insider_logs'].insert(0, new_log)
    session.modified = True

    # Pass the entire history to the template
    logs = session['insider_logs']
    return render_template('insider_threats.html', logs=logs)

import random

@app.route('/app-attacks')
@login_required
def app_attacks():
    # Simulate detection of a new application attack (for demo)
    new_attack = {
        'type': random.choice(['SQLi', 'XSS', 'CSRF']),
        'endpoint': random.choice(['/login', '/profile', '/settings']),
        'status': random.choice(['Blocked', 'Alert']),
        'time': f"2025-06-10 {random.randint(10, 23)}:{random.choice(['00', '15', '30', '45'])}"
    }

    # Initialize history if not present
    if 'app_attack_logs' not in session:
        session['app_attack_logs'] = []

    # Add the new attack to the top of the list
    session['app_attack_logs'].insert(0, new_attack)
    session.modified = True

    # Pass the entire history to the template
    logs = session['app_attack_logs']
    return render_template('app_attacks.html', logs=logs)

@app.route('/malware')
@login_required
def malware():
    return render_template('malware.html', logs=get_random_logs('malware'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        pass
    return render_template('settings.html')

@app.route('/api/attack_data')
@login_required
def api_attack_data():
    return jsonify(get_random_attack_stats())

if __name__ == '__main__':
    app.run(debug=True)
