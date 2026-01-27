
"""
@author: Kiara Chetty
Desktop version of the Electronic Components Database
"""

from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory
import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import sys
import threading
import time
import socket
import smtplib
from email.message import EmailMessage

# =========================
# RESOURCE PATH (PyInstaller)
# =========================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

template_dir = resource_path("templates")
static_dir = resource_path("static")

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = os.environ.get("SECRET_KEY", "dev_key")

# =========================
# TIMEZONE UTILS
# =========================
def now_sast():
    return datetime.now(ZoneInfo("Africa/Johannesburg"))

def format_dt(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def parse_dt(dt_str):
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=ZoneInfo("Africa/Johannesburg"))

# =========================
# SESSION CONFIG (AUTO LOGOUT)
# =========================
@app.before_request
def check_session_timeout():
    max_inactive = 180  # 3 minutes
    last_activity = session.get("last_activity")
    now = now_sast()

    if last_activity:
        last_dt = parse_dt(last_activity)
        elapsed = (now - last_dt).total_seconds()
        if elapsed > max_inactive:
            session.clear()
            return redirect(url_for("login", logout_msg="inactivity"))

    session["last_activity"] = format_dt(now)

# =========================
# EMAIL CONFIGURATION
# =========================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_SENDER = "ukzn.component@gmail.com"
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_ADMIN = "221008769@stu.ukzn.ac.za"

# =========================
# DATABASE CONFIGURATION
# =========================
DB_HOST = os.environ.get("MYSQL_HOST")
DB_USER = os.environ.get("MYSQL_USER")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD")
DB_NAME = os.environ.get("MYSQL_DATABASE")
DB_PORT = int(os.environ.get("MYSQL_PORT", 3306))

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=DictCursor
    )

# =========================
# NETWORK CHECK
# =========================
def is_online():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

# =========================
# EMAIL FUNCTION
# =========================
def send_admin_email(subject, body):
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_ADMIN
        msg["Subject"] = subject
        msg.set_content(body)
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print("Email error:", e)

# =========================
# DAILY EMAIL SCHEDULER
# =========================
def send_daily_summary():
    while True:
        now = now_sast()
        if now.hour == 16 and now.minute == 0:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                today = now.strftime("%Y-%m-%d")

                # COMPONENTS TAKEN
                cursor.execute("""
                    SELECT u.name, u.student_number, c.name AS component, l.quantity, l.timestamp
                    FROM logs l
                    JOIN users u ON l.user_id = u.id
                    JOIN components c ON l.component_id = c.id
                    WHERE DATE(l.timestamp)=%s AND l.emailed=0
                """, (today,))
                logs = cursor.fetchall()
                if logs:
                    body = "COMPONENTS TAKEN TODAY\n\n"
                    for log in logs:
                        body += f"Name: {log['name']}\nStudent: {log['student_number']}\nComponent: {log['component']}\nQty: {log['quantity']}\nTime: {log['timestamp']}\n\n"
                    send_admin_email("Daily Component Summary", body)
                    cursor.execute("UPDATE logs SET emailed=1 WHERE DATE(timestamp)=%s", (today,))
                conn.commit()
                conn.close()
                time.sleep(60)
            except Exception as e:
                print("Scheduler error:", e)
        time.sleep(20)

# =========================
# LOGIN
# =========================
@app.route("/", methods=["GET","POST"])
def login():
    error = None
    logout_msg = request.args.get("logout_msg","")

    if not is_online():
        error = "System is offline. Please check your internet connection."
        return render_template("login.html", groups={}, error=error, logout_msg=logout_msg)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
    except Exception:
        error = "Database is currently unavailable."
        return render_template("login.html", groups={}, error=error, logout_msg=logout_msg)

    cursor.execute("SELECT * FROM components ORDER BY type, name")
    components = cursor.fetchall()
    groups = {}
    for comp in components:
        groups.setdefault(comp["type"] or "Other", []).append(comp)

    if request.method == "POST":
        name = request.form.get("name","").strip()
        student_number = request.form.get("student_number","").strip()
        cursor.execute("SELECT * FROM users WHERE student_number=%s", (student_number,))
        user = cursor.fetchone()

        if user:
            user_id = user["id"]
            role = user["role"] or "student"
        else:
            role = "admin" if student_number=="000000000" else "student"
            cursor.execute("INSERT INTO users (name, student_number, role) VALUES (%s,%s,%s)",
                           (name or "Unknown", student_number, role))
            conn.commit()
            user_id = cursor.lastrowid

        conn.close()

        session["user_id"] = user_id
        session["role"] = role
        session["last_activity"] = format_dt(now_sast())

        return redirect(url_for("admin" if role=="admin" else "home"))

    conn.close()
    return render_template("login.html", groups=groups, error=error, logout_msg=logout_msg)

# =========================
# HOME
# =========================
@app.route("/home")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM components")
    components = cursor.fetchall()
    conn.close()
    return render_template("index.html", components=components)

# =========================
# LOG COMPONENT
# =========================
@app.route("/log", methods=["POST"])
def log():
    if session.get("role")!="student":
        return redirect(url_for("login"))

    timestamp = format_dt(now_sast())
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (user_id, component_id, quantity, timestamp) VALUES (%s,%s,%s,%s)",
        (session["user_id"], request.form.get("component_id"), int(request.form.get("quantity")), timestamp)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

# =========================
# AUTO LOGOUT
# =========================
@app.route("/auto_logout")
def auto_logout():
    session.clear()
    return redirect(url_for("login", logout_msg="inactivity"))

# =========================
# RUN
# =========================
if __name__ == "__main__":
    threading.Thread(target=send_daily_summary, daemon=True).start()
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port)
