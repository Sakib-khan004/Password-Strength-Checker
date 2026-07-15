# 🔐 SecurePass -- Advanced Password Strength Analyzer

SecurePass is a full-stack Flask web application that analyzes password strength using
multiple security heuristics: entropy calculation, policy checks, common-password
detection, dictionary attack simulation, keyboard-pattern detection, and repeated/sequential
character detection. It scores every password from 0-100, gives actionable suggestions,
stores history in SQLite, and provides an admin analytics dashboard with charts.

---

## ✨ Features

- ✅ Password Policy Checker (length, uppercase, lowercase, numbers, special characters)
- ✅ Entropy Calculator (bits of randomness + estimated offline crack time)
- ✅ Password Strength Meter (visual, color-coded)
- ✅ Common Password Detection (checked against a breach/common password list)
- ✅ Dictionary Attack Simulation (direct match, leetspeak, suffix stripping)
- ✅ Keyboard Pattern Detection (`qwerty`, `asdfgh`, `123456`, etc.)
- ✅ Repeated Character Detection (`aaaaaa`, `111111`)
- ✅ Sequential Character Detection (`abcdef`, `123456`)
- ✅ Password Score (0-100) with strength label
- ✅ Actionable Password Suggestions
- ✅ Dark Theme, Responsive UI
- ✅ Downloadable PDF Report (per analysis)
- ✅ Password History stored in SQLite (masked passwords only)
- ✅ Admin Login Authentication
- ✅ Analytics Dashboard -- totals, averages, strength pie chart, entropy trend line chart
- ✅ GitHub-ready documentation

---

## 🛠 Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Database:** SQLite
- **Charts:** Chart.js
- **PDF Generation:** ReportLab
- **Pattern Matching:** Regex

---

## 📂 Project Structure

```
SecurePass/
│
├── app.py                     # Main Flask application (routes, auth, DB)
├── config.py                  # App configuration (secret key, admin creds, paths)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
├── database.db                # SQLite database (auto-created on first run)
│
├── modules/                   # Core analysis engine
│   ├── entropy.py             # Entropy calculation + crack time estimate
│   ├── policy.py              # Policy checker (length, case, digits, symbols)
│   ├── scorer.py              # Combines all checks into final 0-100 score
│   ├── dictionary_attack.py   # Dictionary attack simulation
│   ├── common_password.py     # Common/breached password detection
│   ├── suggestions.py         # Generates improvement suggestions
│   ├── keyboard_pattern.py    # Keyboard-walk pattern detection
│   ├── sequence_detector.py   # Sequential character detection
│   ├── repeat_detector.py     # Repeated character detection
│   └── report.py              # PDF report generator (ReportLab)
│
├── static/
│   ├── style.css              # Dark theme, responsive styling
│   ├── app.js                 # Frontend logic (AJAX calls, rendering)
│   └── logo.png               # App logo (placeholder)
│
├── templates/
│   ├── base.html              # Shared layout/navbar
│   ├── index.html             # Password analyzer page
│   ├── login.html             # Admin login page
│   └── dashboard.html         # Analytics dashboard page
│
├── data/
│   ├── common_passwords.txt   # Common/breached password list
│   └── dictionary.txt         # Dictionary word list for attack simulation
│
└── screenshots/                # Add your own screenshots here for GitHub
```

---

## 🚀 Getting Started

### 1. Clone / download the project
```bash
cd SecurePass
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

The app will start at **http://127.0.0.1:5000**

### 5. Admin Dashboard
Go to **http://127.0.0.1:5000/login**

Default demo credentials (change these in `config.py` before any real deployment):
```
Username: admin
Password: admin123
```

---

## 🎯 How Scoring Works

The final score (0-100) is calculated as:

| Component | Points |
|---|---|
| Policy checks (length, upper, lower, digit, special) | up to 40 (8 each) |
| Entropy (scaled, 90+ bits = full marks) | up to 35 |
| Length bonus (beyond 12 characters) | up to 10 |
| Common password penalty | -40 |
| Dictionary attack vulnerability penalty | -20 |
| Keyboard pattern penalty | -15 |
| Repeated character penalty | -15 |
| Sequential character penalty | -15 |

Final score is clamped between 0 and 100.

**Strength labels:**
- 0-29: Very Weak
- 30-49: Weak
- 50-69: Moderate
- 70-89: Strong
- 90-100: Very Strong

---

## 🔒 Security Notes

- Passwords are **never stored in plaintext** -- only a masked version (`****`) and
  derived metrics (score, entropy, flags) are saved to the database.
- This tool is for **educational and defensive security purposes** -- to help users
  understand what makes passwords weak or strong. It does not perform any real attacks
  against live systems.
- Change `SECRET_KEY`, `ADMIN_USERNAME`, and `ADMIN_PASSWORD` in `config.py` (or via
  environment variables) before deploying anywhere beyond local/personal use.

---

## 📸 Screenshots

Add your own screenshots to the `screenshots/` folder and reference them here, e.g.:

```markdown
![Analyzer Screenshot](screenshots/analyzer.png)
![Dashboard Screenshot](screenshots/dashboard.png)
```

---

## 📄 License

This project is open for educational and personal portfolio use.
