"""
@author: kiara
"""

import os
import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime, timezone, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

DB_HOST = os.environ["MYSQL_HOST"]
DB_USER = os.environ["MYSQL_USER"]
DB_PASSWORD = os.environ["MYSQL_PASSWORD"]
DB_NAME = os.environ["MYSQL_DATABASE"]
DB_PORT = int(os.environ.get("MYSQL_PORT", 3306))

EMAIL_SENDER = os.environ["EMAIL_SENDER"]
EMAIL_ADMIN = os.environ["EMAIL_ADMIN"]
SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]

def get_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=DictCursor
    )

def send_email(subject, body):
    message = Mail(
        from_email=EMAIL_SENDER,
        to_emails=EMAIL_ADMIN,
        subject=subject,
        plain_text_content=body
    )
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    sg.send(message)

def main():
    now = datetime.now(timezone.utc) + timedelta(hours=2)
    today = now.strftime("%Y-%m-%d")

    conn = get_db()
    cur = conn.cursor()

    # COMPONENTS
    cur.execute("""
        SELECT u.name, u.student_number, c.name AS component, l.quantity, l.timestamp
        FROM logs l
        JOIN users u ON l.user_id=u.id
        JOIN components c ON l.component_id=c.id
        WHERE DATE(l.timestamp)=%s AND l.emailed=0
    """, (today,))
    logs = cur.fetchall()

    if logs:
        body = "COMPONENTS TAKEN TODAY\n\n"
        for r in logs:
            body += (
                f"Name: {r['name']}\n"
                f"Student Number: {r['student_number']}\n"
                f"Component: {r['component']}\n"
                f"Quantity: {r['quantity']}\n"
                f"Time: {r['timestamp']}\n\n"
            )
        send_email("Daily Component Summary", body)
        cur.execute("UPDATE logs SET emailed=1 WHERE DATE(timestamp)=%s", (today,))

    # LOANS
    cur.execute("""
        SELECT u.name, u.student_number, lo.item, lo.loan_date
        FROM loans lo
        JOIN users u ON lo.user_id=u.id
        WHERE DATE(lo.loan_date)=%s AND lo.loan_emailed=0
    """, (today,))
    loans = cur.fetchall()

    if loans:
        body = "ITEMS LOANED TODAY\n\n"
        for r in loans:
            body += (
                f"Name: {r['name']}\n"
                f"Student Number: {r['student_number']}\n"
                f"Item: {r['item']}\n"
                f"Loan Date: {r['loan_date']}\n\n"
            )
        send_email("Daily Loan Summary", body)
        cur.execute("UPDATE loans SET loan_emailed=1 WHERE DATE(loan_date)=%s", (today,))

    # RETURNS
    cur.execute("""
        SELECT u.name, u.student_number, lo.item, lo.return_date
        FROM loans lo
        JOIN users u ON lo.user_id=u.id
        WHERE DATE(lo.return_date)=%s
        AND lo.returned=1
        AND lo.return_emailed=0
    """, (today,))
    returns = cur.fetchall()

    if returns:
        body = "ITEMS RETURNED TODAY\n\n"
        for r in returns:
            body += (
                f"Name: {r['name']}\n"
                f"Student Number: {r['student_number']}\n"
                f"Item: {r['item']}\n"
                f"Return Date: {r['return_date']}\n\n"
            )
        send_email("Daily Return Summary", body)
        cur.execute("UPDATE loans SET return_emailed=1 WHERE DATE(return_date)=%s", (today,))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
