"""
@author: Kiara Chetty
Desktop version of the Electronic Components Database
"""

from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory
import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime, timezone, timedelta
import os
import sys
import threading
import time
import socket

# EMAIL IMPORTS
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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
# SESSION CONFIGURATION
# =========================
app.permanent_session_lifetime = timedelta(minutes=3)

# =========================
# EMAIL CONFIGURATION
# =========================
EMAIL_SENDER = os.environ.get("EMAIL_SENDER", "ukzn.component@gmail.com")
EMAIL_ADMIN = os.environ.get("EMAIL_ADMIN", "221008769@stu.ukzn.ac.za")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")  # must be set on Railway

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
# EMAIL FUNCTION (SendGrid)
# =========================
def send_admin_email(subject, body):
    try:
        message = Mail(
            from_email=os.environ.get("EMAIL_SENDER", "ukzn.component@gmail.com"),
            to_emails=os.environ.get("EMAIL_ADMIN", "221008769@stu.ukzn.ac.za"),
            subject=subject,
            plain_text_content=body
        )
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f"[SENDGRID] Email sent! Status code: {response.status_code}")

    except Exception as e:
        print(f"[SENDGRID] Email error: {e}")

# =========================
# DAILY EMAIL SCHEDULER
# =========================
def send_daily_summary():
    last_sent_date = None
    TARGET_HOUR = 3
    TARGET_MINUTE = 27

    while True:
        try:
            now = datetime.now(timezone.utc) + timedelta(hours=2)  # UTC+2
            today = now.strftime("%Y-%m-%d")

            if (
                now.hour == TARGET_HOUR
                and now.minute == TARGET_MINUTE
                and last_sent_date != today
            ):
                print("Sending daily summary email...")

                conn = get_db_connection()
                cursor = conn.cursor()

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
                        body += (
                            f"Name: {log['name']}\n"
                            f"Student Number: {log['student_number']}\n"
                            f"Component: {log['component']}\n"
                            f"Quantity: {log['quantity']}\n"
                            f"Time: {log['timestamp']}\n\n"
                        )
                    send_admin_email("Daily Component Summary", body)
                    cursor.execute(
                        "UPDATE logs SET emailed=1 WHERE DATE(timestamp)=%s",
                        (today,)
                    )

                # ITEMS LOANED
                cursor.execute("""
                    SELECT u.name, u.student_number, lo.item, lo.loan_date
                    FROM loans lo
                    JOIN users u ON lo.user_id = u.id
                    WHERE DATE(lo.loan_date)=%s AND lo.loan_emailed=0
                """, (today,))
                loans = cursor.fetchall()

                if loans:
                    body = "ITEMS LOANED TODAY\n\n"
                    for loan in loans:
                        body += (
                            f"Name: {loan['name']}\n"
                            f"Student Number: {loan['student_number']}\n"
                            f"Item: {loan['item']}\n"
                            f"Loan Date: {loan['loan_date']}\n\n"
                        )
                    send_admin_email("Daily Loan Summary", body)
                    cursor.execute(
                        "UPDATE loans SET loan_emailed=1 WHERE DATE(loan_date)=%s",
                        (today,)
                    )

                # ITEMS RETURNED
                cursor.execute("""
                    SELECT u.name, u.student_number, lo.item, lo.return_date
                    FROM loans lo
                    JOIN users u ON lo.user_id = u.id
                    WHERE DATE(lo.return_date)=%s
                    AND lo.returned=1
                    AND lo.return_emailed=0
                """, (today,))
                returns = cursor.fetchall()

                if returns:
                    body = "ITEMS RETURNED TODAY\n\n"
                    for r in returns:
                        body += (
                            f"Name: {r['name']}\n"
                            f"Student Number: {r['student_number']}\n"
                            f"Item: {r['item']}\n"
                            f"Return Date: {r['return_date']}\n\n"
                        )
                    send_admin_email("Daily Return Summary", body)
                    cursor.execute(
                        "UPDATE loans SET return_emailed=1 WHERE DATE(return_date)=%s",
                        (today,)
                    )

                conn.commit()
                conn.close()
                last_sent_date = today
                print("Daily summary email sent successfully")

            time.sleep(60)

        except Exception as e:
            print("Scheduler error:", e)
            time.sleep(60)

@app.route("/test_sendgrid")
def test_sendgrid():
    send_admin_email("Test Email", "This is a test from SendGrid.")
    return "Check your email!"

# =========================
# LOGIN
# =========================
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    logout_msg = request.args.get("logout_msg", "")

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
        key = comp["type"] or "Other"
        groups.setdefault(key, []).append(comp)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        student_number = request.form.get("student_number", "").strip()

        if not (student_number.isdigit() and len(student_number) == 9) and student_number != "000000000":
            conn.close()
            error = "Student number must be exactly 9 digits (or the admin ID)."
            return render_template("login.html", groups=groups, error=error, logout_msg=logout_msg)

        cursor.execute("SELECT * FROM users WHERE student_number=%s", (student_number,))
        user = cursor.fetchone()

        if user:
            user_id = user["id"]
            if user["name"] != name and name:
                cursor.execute("UPDATE users SET name=%s WHERE id=%s", (name, user_id))
                conn.commit()
            role = user["role"] or "student"
        else:
            role = "admin" if student_number == "000000000" else "student"
            cursor.execute(
                "INSERT INTO users (name, student_number, role) VALUES (%s,%s,%s)",
                (name or "Unknown", student_number, role)
            )
            conn.commit()
            user_id = cursor.lastrowid

        conn.close()
        session.permanent = True
        session["user_id"] = user_id
        session["name"] = name or "User"
        session["student_number"] = student_number
        session["role"] = role
        return redirect(url_for("admin" if role == "admin" else "home"))

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

    query = request.args.get("search", "").strip()

    if query:
        cursor.execute(
            "SELECT * FROM components WHERE name LIKE %s OR description LIKE %s",
            (f"%{query}%", f"%{query}%")
        )
    else:
        cursor.execute("SELECT * FROM components")

    components = cursor.fetchall()
    conn.close()
    return render_template("index.html", components=components)

# =========================
# LOG COMPONENT
# =========================
@app.route("/log", methods=["POST"])
def log():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    component_id = request.form.get("component_id")
    quantity = int(request.form.get("quantity", 0))
    timestamp = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (user_id, component_id, quantity, timestamp) VALUES (%s,%s,%s,%s)",
        (session["user_id"], component_id, quantity, timestamp)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

# =========================
# LOANS
# =========================
@app.route("/loan", methods=["GET", "POST"])
def loan():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        item = request.form.get("item")
        now = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO loans (user_id, item, loan_date) VALUES (%s,%s,%s)",
            (session["user_id"], item, now)
        )
        conn.commit()

    cursor.execute("SELECT * FROM loans WHERE user_id=%s", (session["user_id"],))
    loans = cursor.fetchall()
    conn.close()
    return render_template("loan.html", loans=loans)

# =========================
# RETURN LOAN
# =========================
@app.route("/return_loan/<int:loan_id>")
def return_loan(loan_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    return_time = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "UPDATE loans SET returned=1, return_date=%s WHERE id=%s",
        (return_time, loan_id)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("loan"))

# =========================
# ADMIN
# =========================
@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    search = request.args.get("search", "").strip()
    conn = get_db_connection()
    cursor = conn.cursor()

    if search:
        cursor.execute("""
            SELECT u.name, u.student_number, c.name AS component_name, l.quantity, l.timestamp
            FROM logs l
            JOIN users u ON l.user_id=u.id
            JOIN components c ON l.component_id=c.id
            WHERE u.student_number LIKE %s OR u.name LIKE %s
            ORDER BY l.timestamp DESC
        """, (f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("""
            SELECT u.name, u.student_number, c.name AS component_name, l.quantity, l.timestamp
            FROM logs l
            JOIN users u ON l.user_id=u.id
            JOIN components c ON l.component_id=c.id
            ORDER BY l.timestamp DESC
        """)

    logs = cursor.fetchall()

    if search:
        cursor.execute("""
            SELECT u.name, u.student_number, lo.item, lo.loan_date, lo.returned, lo.return_date
            FROM loans lo
            JOIN users u ON lo.user_id=u.id
            WHERE u.student_number LIKE %s OR u.name LIKE %s
            ORDER BY lo.loan_date DESC
        """, (f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("""
            SELECT u.name, u.student_number, lo.item, lo.loan_date, lo.returned, lo.return_date
            FROM loans lo
            JOIN users u ON lo.user_id=u.id
            ORDER BY lo.loan_date DESC
        """)

    loan_logs = cursor.fetchall()
    conn.close()
    return render_template("admin.html", logs=logs, loan_logs=loan_logs, search=search)

# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login", logout_msg="manual"))

@app.route("/auto_logout")
def auto_logout():
    session.clear()
    return redirect(url_for("login", logout_msg="inactivity"))

# =========================
# DATASHEETS
# =========================
@app.route("/datasheet/<path:filename>")
def datasheet(filename):
    return send_from_directory(static_dir, filename)

# =========================
# RUN
# =========================
if __name__ == "__main__":
    threading.Thread(target=send_daily_summary, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
