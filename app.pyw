"""
@author: Kiara Chetty
Desktop version of the Electronic Components Database
"""

from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory
import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime
import os
import sys

# EMAIL IMPORTS
import smtplib
from email.message import EmailMessage

# =========================
# RESOURCE PATH (PyInstaller)
# =========================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

template_dir = resource_path("templates")
static_dir = resource_path("static")

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = "secret_key"  # change for production


# =========================
# EMAIL CONFIGURATION
# =========================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_SENDER = "ukzn.component@gmail.com"
EMAIL_PASSWORD = ""
EMAIL_ADMIN = "221008769@stu.ukzn.ac.za"

# =========================
# DATABASE CONFIGURATION
# =========================
DB_HOST = "127.0.0.1"
DB_USER = "kiosk_user"
DB_PASSWORD = "Components"
DB_NAME = "component_db"

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=3306,
        cursorclass=DictCursor
    )

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
# LOGIN
# =========================
@app.route("/", methods=["GET", "POST"])
def login():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM components ORDER BY type, name")
    components = cursor.fetchall()

    groups = {}
    for comp in components:
        key = comp["type"] or "Other"
        groups.setdefault(key, []).append(comp)

    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        student_number = request.form.get("student_number", "").strip()

        if not (student_number.isdigit() and len(student_number) == 9) and student_number != "000000000":
            conn.close()
            error = "Student number must be exactly 9 digits (or the admin ID)."
            return render_template("login.html", groups=groups, error=error)

        cursor.execute("SELECT * FROM users WHERE student_number = %s", (student_number,))
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
                "INSERT INTO users (name, student_number, role) VALUES (%s, %s, %s)",
                (name or "Unknown", student_number, role)
            )
            conn.commit()
            user_id = cursor.lastrowid

        conn.close()

        session["user_id"] = user_id
        session["name"] = name or "User"
        session["student_number"] = student_number
        session["role"] = role


        return redirect(url_for("admin" if role == "admin" else "home"))

    conn.close()
    return render_template("login.html", groups=groups, error=error)

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
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM components WHERE id=%s", (component_id,))
    component = cursor.fetchone()

    cursor.execute(
        "INSERT INTO logs (user_id, component_id, quantity, timestamp) VALUES (%s,%s,%s,%s)",
        (session["user_id"], component_id, quantity, timestamp)
    )
    conn.commit()
    conn.close()

    send_admin_email(
        "Component Taken",
        f"""
Student Name: {session['name']}
Student Number: {session['student_number']}
Component: {component['name']}
Quantity: {quantity}
Date & Time: {timestamp}
"""
    )

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
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO loans (user_id, item, loan_date) VALUES (%s,%s,%s)",
            (session["user_id"], item, now)
        )
        conn.commit()

        send_admin_email(
            "Item Loaned",
            f"""
Student Name: {session['name']}
Student Number: {session['student_number']}
Item: {item}
Loan Date: {now}
"""
        )

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

    cursor.execute("SELECT item FROM loans WHERE id=%s", (loan_id,))
    loan = cursor.fetchone()

    return_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "UPDATE loans SET returned=1, return_date=%s WHERE id=%s",
        (return_time, loan_id)
    )
    conn.commit()
    conn.close()

    send_admin_email(
        "Item Returned",
        f"""
Student Name: {session['name']}
Student Number: {session['student_number']}
Item: {loan['item']}
Return Date: {return_time}
"""
    )

    return redirect(url_for("loan"))

# =========================
# ADMIN
# =========================
@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT u.name, u.student_number, c.name AS component_name, l.quantity, l.timestamp
        FROM logs l
        JOIN users u ON l.user_id = u.id
        JOIN components c ON l.component_id = c.id
        ORDER BY l.timestamp DESC
    """)
    logs = cursor.fetchall()

    cursor.execute("""
        SELECT u.name, u.student_number, lo.item, lo.loan_date, lo.returned, lo.return_date
        FROM loans lo
        JOIN users u ON lo.user_id = u.id
        ORDER BY lo.loan_date DESC
    """)
    loan_logs = cursor.fetchall()

    conn.close()
    return render_template("admin.html", logs=logs, loan_logs=loan_logs)

# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

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
    app.run(host="0.0.0.0", port=5000)
