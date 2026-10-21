import os
import re
import requests
from bs4 import BeautifulSoup

# URLs for Inverters R Us Clearance
OPEN_BOX_URL = "https://invertersrus.com/victron-energy-b-stock-sale/"
USED_URL = "https://invertersrus.com/used-victron-energy-sale/"

# Updated target items for remaining RV build components & max target prices
TARGETS = {
    # Rooftop MPPT Charge Controller (910W Array)
    "150/60": {"name": "SmartSolar MPPT 150/60", "max_price": 260.0},
    "150|60": {"name": "SmartSolar MPPT 150/60", "max_price": 260.0},
    "scc115060": {"name": "SmartSolar MPPT 150/60", "max_price": 260.0},
    
    # Ground Port MPPT Charge Controller
    "100/20": {"name": "SmartSolar MPPT 100/20", "max_price": 75.0},
    "100|20": {"name": "SmartSolar MPPT 100/20", "max_price": 75.0},
    "scc110020": {"name": "SmartSolar MPPT 100/20", "max_price": 75.0},
    
    # System Monitoring
    "cerbo": {"name": "Cerbo GX", "max_price": 180.0},
    "touch 50": {"name": "GX Touch 50", "max_price": 140.0},
    "touch 70": {"name": "GX Touch 70", "max_price": 180.0},
    
    # DC Power Distribution
    "lynx power-in": {"name": "Lynx Power-In", "max_price": 90.0},
    "lynx distributor": {"name": "Lynx Distributor", "max_price": 120.0},
    "lyn020102000": {"name": "Lynx Power-In", "max_price": 90.0},
    "lyn060102000": {"name": "Lynx Distributor", "max_price": 120.0},
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def send_alert(message):
    print(f"ALERT TRIGGERED: {message}")
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if webhook_url:
        try:
            requests.post(webhook_url, json={"content": message}, timeout=10)
            print("Successfully sent Discord webhook notification!")
        except Exception as e:
            print(f"Failed to send webhook: {e}")

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
                    # Verify it's in stock
                    if "out of stock" not in text and ("in stock" in text or "buy" in text or "add to cart" in text):
                        price_match = re.search(r'\$(\d+(?:\.\d{2})?)', text)
                        if price_match:
                            price = float(price_match.group(1))
                            if price <= target["max_price"]:
                                msg = f"🚨 **VICTRON DEAL FOUND [{page_type}]** 🚨\n**Item:** {target['name']}\n**Price:** ${price:.2f} (Target: <=${target['max_price']:.2f})\n**Link:** {url}"
                                send_alert(msg)
                                found_count += 1
                                
        print(f"Finished checking {page_type}. Deals matched: {found_count}")
        
    except Exception as e:
        print(f"Error checking {page_type}: {e}")

if __name__ == "__main__":
    print("Starting Victron Inventory Radar Scan...")
    check_page(OPEN_BOX_URL, "Open-Box")
    check_page(USED_URL, "Used")
    print("Scan complete.")
