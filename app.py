import sqlite3
from datetime import datetime
from functools import wraps

from flask import (Flask, render_template, request, jsonify, session,
                    redirect, url_for, send_file, flash)

from config import Config
from modules.scorer import analyze_password
from modules.report import generate_pdf_report

app = Flask(__name__)
app.config.from_object(Config)


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------
def get_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS password_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password_masked TEXT NOT NULL,
            score INTEGER NOT NULL,
            strength TEXT NOT NULL,
            entropy REAL NOT NULL,
            is_common INTEGER NOT NULL,
            has_keyboard_pattern INTEGER NOT NULL,
            has_repeat INTEGER NOT NULL,
            has_sequence INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_to_history(analysis: dict):
    conn = get_db()
    conn.execute(
        """INSERT INTO password_history
           (password_masked, score, strength, entropy, is_common,
            has_keyboard_pattern, has_repeat, has_sequence, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            analysis["password_masked"],
            analysis["score"],
            analysis["strength"],
            analysis["entropy"],
            int(analysis["common_password"]["is_common"]),
            int(analysis["keyboard_pattern"]["detected"]),
            int(analysis["repeated_chars"]["detected"]),
            int(analysis["sequential_chars"]["detected"]),
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ---------------------------------------------------------------------------
# Routes -- Core Analyzer
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")

    if not password:
        return jsonify({"error": "Password is required."}), 400

    analysis = analyze_password(
        password,
        common_pw_file=app.config["COMMON_PASSWORDS_FILE"],
        dictionary_file=app.config["DICTIONARY_FILE"],
    )

    if "error" in analysis:
        return jsonify(analysis), 400

    # store a copy (with the real password kept only in-memory for the PDF button)
    session["last_analysis"] = analysis
    save_to_history(analysis)

    return jsonify(analysis)


@app.route("/report/pdf", methods=["POST"])
def download_report():
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")

    if not password:
        return jsonify({"error": "Password is required."}), 400

    analysis = analyze_password(
        password,
        common_pw_file=app.config["COMMON_PASSWORDS_FILE"],
        dictionary_file=app.config["DICTIONARY_FILE"],
    )

    pdf_buffer = generate_pdf_report(analysis)
    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="SecurePass_Report.pdf",
    )


# ---------------------------------------------------------------------------
# Routes -- Auth
# ---------------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == app.config["ADMIN_USERNAME"] and password == app.config["ADMIN_PASSWORD"]:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ---------------------------------------------------------------------------
# Routes -- Dashboard / Analytics
# ---------------------------------------------------------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db()
    rows = conn.execute("SELECT * FROM password_history ORDER BY id DESC LIMIT 200").fetchall()
    conn.close()

    total_tested = len(rows)
    avg_score = round(sum(r["score"] for r in rows) / total_tested, 1) if total_tested else 0
    weak_count = sum(1 for r in rows if r["strength"] in ("Very Weak", "Weak"))
    strong_count = sum(1 for r in rows if r["strength"] in ("Strong", "Very Strong"))
    weak_pct = round((weak_count / total_tested) * 100, 1) if total_tested else 0
    strong_pct = round((strong_count / total_tested) * 100, 1) if total_tested else 0

    strength_counts = {"Very Weak": 0, "Weak": 0, "Moderate": 0, "Strong": 0, "Very Strong": 0}
    for r in rows:
        strength_counts[r["strength"]] = strength_counts.get(r["strength"], 0) + 1

    entropy_history = [r["entropy"] for r in reversed(rows[:30])]
    entropy_labels = [f"#{i+1}" for i in range(len(entropy_history))]

    stats = {
        "total_tested": total_tested,
        "avg_score": avg_score,
        "weak_pct": weak_pct,
        "strong_pct": strong_pct,
        "strength_counts": strength_counts,
        "entropy_history": entropy_history,
        "entropy_labels": entropy_labels,
    }

    return render_template("dashboard.html", stats=stats, rows=rows[:50])


@app.route("/api/dashboard-data")
@login_required
def api_dashboard_data():
    conn = get_db()
    rows = conn.execute("SELECT * FROM password_history ORDER BY id DESC LIMIT 200").fetchall()
    conn.close()

    strength_counts = {"Very Weak": 0, "Weak": 0, "Moderate": 0, "Strong": 0, "Very Strong": 0}
    for r in rows:
        strength_counts[r["strength"]] = strength_counts.get(r["strength"], 0) + 1

    entropy_history = [r["entropy"] for r in reversed(rows[:30])]

    return jsonify({
        "strength_counts": strength_counts,
        "entropy_history": entropy_history,
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5050)
