import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup

# URLs for Inverters R Us Clearance
OPEN_BOX_URL = "https://invertersrus.com/victron-energy-b-stock-sale/"
USED_URL = "https://invertersrus.com/used-victron-energy-sale/"

TARGETS = {
    "150/60": {"name": "SmartSolar MPPT 150/60", "max_price": 260.0},
    "150|60": {"name": "SmartSolar MPPT 150/60", "max_price": 260.0},
    "scc115060": {"name": "SmartSolar MPPT 150/60", "max_price": 260.0},
    "100/20": {"name": "SmartSolar MPPT 100/20", "max_price": 75.0},
    "100|20": {"name": "SmartSolar MPPT 100/20", "max_price": 75.0},
    "scc110020": {"name": "SmartSolar MPPT 100/20", "max_price": 75.0},
    "cerbo": {"name": "Cerbo GX", "max_price": 180.0},
    "touch 50": {"name": "GX Touch 50", "max_price": 140.0},
    "touch 70": {"name": "GX Touch 70", "max_price": 180.0},
    "lynx power-in": {"name": "Lynx Power-In", "max_price": 90.0},
    "lynx distributor": {"name": "Lynx Distributor", "max_price": 120.0},
    "lyn020102000": {"name": "Lynx Power-In", "max_price": 90.0},
    "lyn060102000": {"name": "Lynx Distributor", "max_price": 120.0},
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def send_email_alert(subject, body):
    print(f"ALERT TRIGGERED: {subject}")
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    receiver_email = os.environ.get("RECEIVER_EMAIL")

    if not (sender_email and sender_password and receiver_email):
        print("Missing email environment variables. Cannot send notification.")
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Successfully sent email notification!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_page(url, page_type):
    print(f"Checking {page_type} page: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            print(f"Failed to load page. Status code: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("tr")
        found_count = 0
        
        for row in rows:
            text = row.get_text().lower()
            for key, target in TARGETS.items():
                if key in text:
                    if "out of stock" not in text and ("in stock" in text or "buy" in text or "add to cart" in text):
                        price_match = re.search(r'\$(\d+(?:\.\d{2})?)', text)
                        if price_match:
                            price = float(price_match.group(1))
                            if price <= target["max_price"]:
                                subject = f"Victron Deal Found: {target['name']} (${price:.2f})"
                                body = f"🚨 VICTRON DEAL FOUND [{page_type}] 🚨\nItem: {target['name']}\nPrice: ${price:.2f} (Target: <=${target['max_price']:.2f})\nLink: {url}"
                                send_email_alert(subject, body)
                                found_count += 1
                                
        print(f"Finished checking {page_type}. Deals matched: {found_count}")
        
    except Exception as e:
        print(f"Error checking {page_type}: {e}")

if __name__ == "__main__":
    print("Starting Victron Inventory Radar Scan...")
    check_page(OPEN_BOX_URL, "Open-Box")
    check_page(USED_URL, "Used")
    print("Scan complete.")
