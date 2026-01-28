from datetime import datetime, timezone, timedelta
import os
import pymysql
from pymysql.cursors import DictCursor
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# -----------------------------
# Environment variables
# -----------------------------
EMAIL_SENDER = os.environ["EMAIL_SENDER"]
EMAIL_ADMIN = os.environ["EMAIL_ADMIN"]
SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]

DB_HOST = os.environ["MYSQL_HOST"]
DB_USER = os.environ["MYSQL_USER"]
DB_PASSWORD = os.environ["MYSQL_PASSWORD"]
DB_NAME = os.environ["MYSQL_DATABASE"]
DB_PORT = int(os.environ.get("MYSQL_PORT", 3306))

# -----------------------------
# DB connection
# -----------------------------
def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=DictCursor
    )

# -----------------------------
# Send email
# -----------------------------
def send_admin_email(subject, body):
    try:
        message = Mail(
            from_email=EMAIL_SENDER,
            to_emails=EMAIL_ADMIN,
            subject=subject,
            plain_text_content=body
        )
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"[SENDGRID] Email sent! Status code: {response.status_code}")
    except Exception as e:
        print(f"[SENDGRID] Email error: {e}")

# -----------------------------
# Main function
# -----------------------------
def send_daily_summary_once():
    conn = get_db_connection()
    cursor = conn.cursor()

    today = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%Y-%m-%d")  # SAST

    # Example: components taken today
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
            body += f"{log['name']} | {log['student_number']} | {log['component']} | {log['quantity']} | {log['timestamp']}\n"
        send_admin_email("Daily Component Summary", body)
        cursor.execute("UPDATE logs SET emailed=1 WHERE DATE(timestamp)=%s", (today,))

    conn.commit()
    conn.close()
    print("Daily summary finished.")

if __name__ == "__main__":
    send_daily_summary_once()
