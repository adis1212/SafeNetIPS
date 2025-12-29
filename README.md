# SafeNetIPS

**Flask • Machine Learning • Intrusion Prevention System**

SafeNetIPS is a Flask-based AI-powered Intrusion Prevention System (IPS) designed to detect and prevent cyber attacks such as phishing emails, brute-force logins, insider threats, malware, and application-layer attacks using machine learning and simulated real-time threat analysis.

---

## Key features

* Real-time intrusion detection using a trained ML model (`intrusion_model.pkl`)
* Blocks malicious IPs (managed via `blocked_ips.txt`)
* Simulated threat analysis and alerting
* Simple Flask web UI with authentication (login) and admin dashboard

---

## Screenshots

> Place three images inside the `screenshots/` folder with the exact filenames below, or update the paths inside this README to match your filenames.

### 1) Website / Home page

![Website Screenshot](screenshots/website.png)

*Caption: Main landing / status page of SafeNetIPS.*

### 2) Login / Authentication

![Login Screenshot](screenshots/login.png)

*Caption: Login page showing authentication form and sample validation.*

### 3) Dashboard / Features

![Dashboard Screenshot](screenshots/dashboard.png)

*Caption: Admin dashboard showing detected events, blocked IPs and model stats.*

---

## Quick start

1. Clone the repo:

```bash
git clone https://github.com/adis1212/SafeNetIPS.git
cd SafeNetIPS
```

2. (Recommended) Create a virtual environment and activate it:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. Install dependencies

> If you have a `requirements.txt` file, run `pip install -r requirements.txt`. If not, install common dependencies used by Flask ML apps:

```bash
pip install flask scikit-learn pandas numpy
```

4. Run the app:

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

---

## Project structure (high level)

```
SafeNetIPS/
├─ app.py                  # Flask app entrypoint
├─ intrusion_model.pkl     # Trained ML model used for detection
├─ blocked_ips.txt         # Manual/auto-blocked IPs
├─ templates/              # HTML templates for website, login, dashboard
├─ static/                 # CSS, JS, images
└─ screenshots/            # Add the 3 screenshots here
```

---

## How to add / replace the screenshots

1. Save your three screenshots using these filenames inside the `screenshots/` folder:

   * `website.png` — screenshot of the main/site page
     ![Features](https://github.com/user-attachments/assets/fbe7b947-ef27-4422-bc5e-23f32df416fe)

   * `login.png` — screenshot of the login/authentication page
     ![Login](https://github.com/user-attachments/assets/722ac224-0eea-4cc4-8b35-9653499bd819)

   * `dashboard.png` — screenshot of the dashboard/features page
     ![Dashboard](https://github.com/user-attachments/assets/34e4ea01-cced-4607-a636-4c621cd843d6)


2. Commit and push:

```bash
git add screenshots/website.png screenshots/login.png screenshots/dashboard.png README.md
git commit -m "Add README + screenshots"
git push origin main
```

---

## Notes & tips

* If your web UI uses different image names or locations, update the image paths above to match.
* For production, do **not** run Flask’s development server publicly — use a production WSGI server (gunicorn/uvicorn) behind a reverse proxy.
* Consider adding a `requirements.txt` file and a short `CONTRIBUTING.md` for contributors.

---

## Contributing

PRs welcome — open an issue or submit a pull request with the change and a short description.

---

## License

MIT License.

---

## Contact

Created by `adis1212` — feel free to open issues on the repo for questions or feature requests.
