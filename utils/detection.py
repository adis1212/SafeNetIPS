import joblib
import numpy as np

model = joblib.load('model/intrusion_model.pkl')

def detect_intrusion(data):
    features = np.array([
        data['packet_size'],
        data['num_requests'],
        data['src_ip_entropy'],
        data['sql_keywords'],
        data['xss_payloads'],
        data['csrf_tokens'],
        data['brute_force_attempts'],
        data['phishing_links'],
        data['spyware_signals'],
        data['insider_flags']
    ]).reshape(1, -1)

    prediction = model.predict(features)[0]
    return {
        'intrusion': bool(prediction),
        'attack_type': 'Detected' if prediction else 'None',
        'ip': data['ip']
    }
