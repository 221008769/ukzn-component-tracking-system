import threading
import webview
import time
import os
import sys
from app import app  # your Flask app

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    time.sleep(2)
    webview.create_window(
        "UKZN Component Tracking System",
        "http://192.168.1.14:5000",  # use your LAN IP
        fullscreen=True,
        resizable=False
    )
    webview.start()
