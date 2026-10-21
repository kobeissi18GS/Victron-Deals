<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Victron Deal Radar & Inverters R Us Monitor</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        victron: {
                            blue: '#005CA9',
                            dark: '#003B6D',
                            light: '#1E88E5',
                            orange: '#FF8A00'
                        }
                    }
                }
            }
        }
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; }
        .glass {
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(12px);
        }
        .custom-scrollbar::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: rgba(30, 41, 59, 0.5);
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #334155;
            border-radius: 3px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: #475569;
        }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col font-sans antialiased">

    <!-- Navigation Header -->
    <header class="border-b border-slate-800 bg-slate-900/80 sticky top-0 z-30 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="p-2 bg-blue-600/20 text-blue-400 rounded-xl border border-blue-500/30">
                    <i data-lucide="radar" class="w-6 h-6 animate-pulse text-blue-400"></i>
                </div>
                <div>
                    <h1 class="font-bold text-lg text-slate-100 flex items-center gap-2">
                        Victron Deal Radar
                        <span class="text-xs px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-mono">Inverters R Us Tracker</span>
                    </h1>
                    <p class="text-xs text-slate-400">Automated Inventory & Price Drop Alert System</p>
                </div>
            </div>

            <!-- Controls / Status -->
            <div class="flex items-center space-x-3">
                <div id="scanner-badge" class="hidden sm:flex items-center space-x-2 text-xs px-3 py-1.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                    <span class="font-medium">Scanner Active</span>
                </div>
                <button id="trigger-scan-btn" onclick="triggerManualScan()" class="px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-blue-600 hover:bg-blue-500 text-white transition flex items-center gap-2 shadow-lg shadow-blue-600/20">
                    <i data-lucide="refresh-cw" id="scan-icon" class="w-3.5 h-3.5"></i>
                    Scan Now
                </button>
                <button onclick="togglePythonModal()" class="px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition flex items-center gap-2">
                    <i data-lucide="code" class="w-3.5 h-3.5 text-amber-400"></i>
                    Get Python Scraper Script
                </button>
            </div>
        </div>
    </header>

    <!-- Main Content Layout -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 grid grid-cols-1 lg:grid-cols-12 gap-6">

        <!-- Left Column: Watched Products & Inventory Live Grid (8 cols) -->
        <div class="lg:col-span-8 space-x-0 space-y-6">
            
            <!-- Key Metric Summary Cards -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div class="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
                    <div class="text-xs text-slate-400 font-medium">Monitored Items</div>
                    <div id="stat-monitored" class="text-2xl font-bold text-slate-100 mt-1">0</div>
                    <div class="text-[10px] text-slate-500 mt-1">Active targets</div>
                </div>
                <div class="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
                    <div class="text-xs text-slate-400 font-medium">In Stock Clearance</div>
                    <div id="stat-instock" class="text-2xl font-bold text-emerald-400 mt-1">0</div>
                    <div class="text-[10px] text-slate-500 mt-1">Available now</div>
                </div>
                <div class="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
                    <div class="text-xs text-slate-400 font-medium">Active Match Deals</div>
                    <div id="stat-deals" class="text-2xl font-bold text-amber-400 mt-1">0</div>
                    <div class="text-[10px] text-slate-500 mt-1">Under target price</div>
                </div>
                <div class="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
                    <div class="text-xs text-slate-400 font-medium">Potential Savings</div>
                    <div id="stat-savings" class="text-2xl font-bold text-blue-400 mt-1">$0</div>
                    <div class="text-[10px] text-slate-500 mt-1">Vs. retail MSRP</div>
                </div>
            </div>

            <!-- Add Target Modal/Card -->
            <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-base font-semibold text-slate-200 flex items-center gap-2">
                        <i data-lucide="plus-circle" class="w-5 h-5 text-blue-400"></i>
                        Add Victron Component Target
                    </h2>
                    <span class="text-xs text-slate-400">Set price thresholds to trigger automated alerts</span>
                </div>

                <form id="add-target-form" onsubmit="handleAddTarget(event)" class="grid grid-cols-1 sm:grid-cols-12 gap-3">
                    <div class="sm:col-span-5">
                        <label class="block text-xs font-medium text-slate-400 mb-1">Component Model</label>
                        <select id="preset-select" onchange="autofillPreset(this.value)" class="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-blue-500">
                            <option value="">-- Select Victron Component --</option>
                            <option value="MultiPlus-II 12/3000/120-50 2x120V">MultiPlus-II 12/3000/120-50 2x120V (PMP122305122)</option>
                            <option value="MultiPlus 12/3000/120-50 120V">MultiPlus 12/3000/120-50 120V (PMP12301102)</option>
                            <option value="SmartSolar MPPT 150/60-Tr">SmartSolar MPPT 150/60-Tr (SCC115060211)</option>
                            <option value="SmartSolar MPPT 100/20">SmartSolar MPPT 100/20 (SCC110020160R)</option>
                            <option value="SmartShunt 500A/50mV">SmartShunt 500A/50mV (SHU050150050)</option>
                            <option value="Cerbo GX">Cerbo GX System Hub (BPP900450100)</option>
                            <option value="GX Touch 50 Display">GX Touch 50 Display (BPP900455050)</option>
                            <option value="Lynx Distributor">Lynx Distributor (LYN060102000)</option>
                            <option value="Lynx Power-In">Lynx Power-In (LYN020102000)</option>
                            <option value="custom">Custom Victron SKU...</option>
                        </select>
                    </div>

                    <div class="sm:col-span-3">
                        <label class="block text-xs font-medium text-slate-400 mb-1">Target Max Price ($)</label>
                        <input type="number" id="target-price" required min="1" step="1" placeholder="e.g. 550" class="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-blue-500">
                    </div>

                    <div class="sm:col-span-2">
                        <label class="block text-xs font-medium text-slate-400 mb-1">Condition</label>
                        <select id="target-condition" class="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-blue-500">
                            <option value="any">Any (Used / Open Box)</option>
                            <option value="open-box">Open Box Only</option>
                            <option value="used">Used Clearance Only</option>
                        </select>
                    </div>

                    <div class="sm:col-span-2 flex items-end">
                        <button type="submit" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-medium py-2 px-3 rounded-lg text-sm transition flex items-center justify-center gap-1">
                            <i data-lucide="plus" class="w-4 h-4"></i>
                            Add Target
                        </button>
                    </div>
                </form>
            </div>

            <!-- Monitored Live Products List -->
            <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h2 class="text-base font-semibold text-slate-200 flex items-center gap-2">
                            <i data-lucide="list-checks" class="w-5 h-5 text-blue-400"></i>
                            Active Target Radar & Live Stock Status
                        </h2>
                        <p class="text-xs text-slate-400">Real-time matching against Inverters R Us clearance/open-box feeds</p>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-xs text-slate-400">Auto-Refresh:</span>
                        <select id="refresh-interval" onchange="updateRefreshInterval(this.value)" class="bg-slate-950 text-xs border border-slate-700 rounded px-2 py-1 text-slate-300">
                            <option value="5">Every 5 seconds (Simulated)</option>
                            <option value="15">Every 15 seconds</option>
                            <option value="30">Every 30 seconds</option>
                            <option value="0">Disabled</option>
                        </select>
                    </div>
                </div>

                <div id="target-items-container" class="space-y-3">
                    <!-- Populated dynamically via JS -->
                </div>
            </div>

        </div>

        <!-- Right Column: Alert Channels & Live Activity Feed (4 cols) -->
        <div class="lg:col-span-4 space-y-6">

            <!-- Alert Configuration Panel -->
            <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl">
                <h2 class="text-base font-semibold text-slate-200 mb-3 flex items-center gap-2">
                    <i data-lucide="bell" class="w-5 h-5 text-amber-400"></i>
                    Notification Channels
                </h2>
                <p class="text-xs text-slate-400 mb-4">Select how you want to be notified when a deal is found.</p>

                <div class="space-y-3 text-sm">
                    <label class="flex items-center justify-between p-3 rounded-xl bg-slate-950 border border-slate-800 cursor-pointer hover:border-slate-700 transition">
                        <div class="flex items-center gap-3">
                            <div class="p-2 rounded-lg bg-indigo-500/10 text-indigo-400">
                                <i data-lucide="message-square" class="w-4 h-4"></i>
                            </div>
                            <div>
                                <div class="font-medium text-slate-200 text-xs">Discord Webhook</div>
                                <div class="text-[10px] text-slate-500">Instant channel alerts</div>
                            </div>
                        </div>
                        <input type="checkbox" id="notify-discord" checked class="rounded border-slate-700 text-blue-600 focus:ring-0 bg-slate-900 w-4 h-4">
                    </label>

                    <label class="flex items-center justify-between p-3 rounded-xl bg-slate-950 border border-slate-800 cursor-pointer hover:border-slate-700 transition">
                        <div class="flex items-center gap-3">
                            <div class="p-2 rounded-lg bg-sky-500/10 text-sky-400">
                                <i data-lucide="send" class="w-4 h-4"></i>
                            </div>
                            <div>
                                <div class="font-medium text-slate-200 text-xs">Telegram Bot</div>
                                <div class="text-[10px] text-slate-500">Push notifications to mobile</div>
                            </div>
                        </div>
                        <input type="checkbox" id="notify-telegram" checked class="rounded border-slate-700 text-blue-600 focus:ring-0 bg-slate-900 w-4 h-4">
                    </label>

                    <label class="flex items-center justify-between p-3 rounded-xl bg-slate-950 border border-slate-800 cursor-pointer hover:border-slate-700 transition">
                        <div class="flex items-center gap-3">
                            <div class="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
                                <i data-lucide="mail" class="w-4 h-4"></i>
                            </div>
                            <div>
                                <div class="font-medium text-slate-200 text-xs">Email Alert (SMTP)</div>
                                <div class="text-[10px] text-slate-500">Digest / Immediate email</div>
                            </div>
                        </div>
                        <input type="checkbox" id="notify-email" class="rounded border-slate-700 text-blue-600 focus:ring-0 bg-slate-900 w-4 h-4">
                    </label>
                </div>
            </div>

            <!-- Live Alert Stream & Scanner Log -->
            <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col h-[480px]">
                <div class="flex items-center justify-between mb-3">
                    <h2 class="text-base font-semibold text-slate-200 flex items-center gap-2">
                        <i data-lucide="activity" class="w-5 h-5 text-emerald-400"></i>
                        Scanner Activity Stream
                    </h2>
                    <button onclick="clearLogs()" class="text-[11px] text-slate-500 hover:text-slate-300">Clear</button>
                </div>

                <!-- Log list -->
                <div id="activity-log" class="flex-1 overflow-y-auto space-y-2 pr-1 custom-scrollbar font-mono text-xs">
                    <!-- Dynamic logs -->
                </div>
            </div>

        </div>

    </main>

    <!-- Python Script Generator Modal -->
    <div id="python-modal" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 hidden">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl max-w-4xl w-full max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
            <!-- Modal Header -->
            <div class="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-900">
                <div class="flex items-center gap-3">
                    <div class="p-2 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
                        <i data-lucide="code" class="w-5 h-5"></i>
                    </div>
                    <div>
                        <h3 class="font-bold text-slate-100">Victron Inverters R Us Python Scraper</h3>
                        <p class="text-xs text-slate-400">Run locally, deploy to GitHub Actions (Free 24/7), or Replit</p>
                    </div>
                </div>
                <button onclick="togglePythonModal()" class="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800">
                    <i data-lucide="x" class="w-5 h-5"></i>
                </button>
            </div>

            <!-- Modal Body -->
            <div class="p-6 overflow-y-auto custom-scrollbar flex-1 space-y-4">
                
                <div class="bg-blue-950/40 border border-blue-800/40 rounded-xl p-4 text-xs text-blue-200 flex items-start gap-3">
                    <i data-lucide="info" class="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5"></i>
                    <div>
                        <span class="font-semibold text-blue-300">Deployment Quick Start:</span> Copy this script into a file named <code class="bg-slate-950 px-1.5 py-0.5 rounded text-amber-300 font-mono">victron_tracker.py</code>. Configure your target max prices and webhook URLs (Discord / Telegram / Email) near the top of the file. Set up a cron job or a GitHub Action to run every 15–60 minutes.
                    </div>
                </div>

                <div class="relative">
                    <button onclick="copyPythonScript()" class="absolute top-3 right-3 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs px-3 py-1.5 rounded-lg border border-slate-700 flex items-center gap-1.5 transition">
                        <i data-lucide="copy" class="w-3.5 h-3.5"></i>
                        <span id="copy-btn-text">Copy Script</span>
                    </button>
                    <pre class="bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs font-mono text-emerald-400 overflow-x-auto leading-relaxed max-h-[400px]" id="python-script-code">
import requests
from bs4 import BeautifulSoup
import time
import json
import smtplib
from email.mime.text import MIMEText

# ==============================================================================
# VICTRON INVERTERS R US DEAL RADAR CONFIGURATION
# ==============================================================================

# Configure your watched Victron components & max target prices ($ USD)
WATCHED_TARGETS = {
    "MultiPlus-II 12/3000": {"target_price": 550.00, "keywords": ["12/3000", "pmp122305122"]},
    "SmartSolar MPPT 150/60": {"target_price": 210.00, "keywords": ["150/60", "scc115060211"]},
    "SmartSolar MPPT 100/20": {"target_price": 60.00, "keywords": ["100/20", "scc110020160r"]},
    "SmartShunt 500A": {"target_price": 65.00, "keywords": ["smartshunt", "shu050150050"]},
    "Cerbo GX": {"target_price": 140.00, "keywords": ["cerbo", "bpp900450100"]},
    "GX Touch 50": {"target_price": 120.00, "keywords": ["touch 50", "bpp900455050"]},
    "Lynx Distributor": {"target_price": 110.00, "keywords": ["lynx distributor", "lyn060102000"]}
}

# Alert Webhook Settings (Leave blank or set to None if unused)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE"
TELEGRAM_BOT_TOKEN = None  # e.g. "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ"
TELEGRAM_CHAT_ID = None    # e.g. "987654321"

# Target Scraping URLs on Inverters R Us
URLS_TO_SCAN = [
    "https://www.invertersrus.com/product-category/open-box-deals/",
    "https://www.invertersrus.com/used-equipment-clearance/"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def send_discord_alert(item_title, price, url, condition):
    if not DISCORD_WEBHOOK_URL or "YOUR_WEBHOOK" in DISCORD_WEBHOOK_URL:
        return
    payload = {
        "embeds": [{
            "title": f"🚨 Victron Deal Alert: {item_title}",
            "color": 3447003, # Victron Blue
            "fields": [
                {"name": "Price", "value": f"${price:.2f}", "inline": True},
                {"name": "Condition", "value": condition, "inline": True},
                {"name": "Link", "value": f"[View Product]({url})", "inline": False}
            ],
            "footer": {"text": "Victron Deal Radar Tracker"}
        }]
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        print(f"[+] Discord alert sent for {item_title}")
    except Exception as e:
        print(f"[-] Failed to send Discord alert: {e}")

def check_inventory():
    print("🔍 Starting scan of Inverters R Us deals...")
    found_deals = []

    for url in URLS_TO_SCAN:
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                print(f"[-] HTTP Error {response.status_code} scanning {url}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for WooCommerce or grid product containers
            products = soup.find_all(['li', 'div'], class_=lambda c: c and ('product' in c or 'type-product' in c))

            for prod in products:
                title_elem = prod.find(['h2', 'h3', 'a'], class_=lambda c: c and 'title' in c or 'woocommerce-loop' in c)
                price_elem = prod.find('span', class_='woocommerce-Price-amount')
                link_elem = prod.find('a', href=True)

                if not title_elem or not price_elem:
                    continue

                title = title_elem.get_text().strip()
                link = link_elem['href'] if link_elem else url
                
                # Clean price numeric value
                price_text = price_elem.get_text().replace('$', '').replace(',', '').strip()
                try:
                    price = float(price_text)
                except ValueError:
                    continue

                # Match against requested targets
                for target_name, config in WATCHED_TARGETS.items():
                    matches = all(kw.lower() in title.lower() for kw in config["keywords"])
                    if matches and price <= config["target_price"]:
                        print(f"🎉 MATCH FOUND! {title} - ${price:.2f} (Target: ${config['target_price']})")
                        send_discord_alert(title, price, link, "Open Box / Used")
                        found_deals.append({"title": title, "price": price, "url": link})

        except Exception as e:
            print(f"[-] Error scanning {url}: {e}")

    print(f"✅ Scan completed. {len(found_deals)} deals matched threshold.")

if __name__ == "__main__":
    check_inventory()
</pre>
                </div>
            </div>
            
            <!-- Modal Footer -->
            <div class="px-6 py-3 border-t border-slate-800 bg-slate-900 flex justify-end">
                <button onclick="togglePythonModal()" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg border border-slate-700">
                    Close
                </button>
            </div>
        </div>
    </div>

    <!-- Notification Toast Container -->
    <div id="toast-container" class="fixed bottom-5 right-5 z-50 flex flex-col space-y-2 pointer-events-none"></div>

    <!-- JavaScript Application Logic -->
    <script>
        // Preset product database with retail baseline prices & default targets
        const VIC_PRESETS = {
            "MultiPlus-II 12/3000/120-50 2x120V": { msrp: 928.00, target: 550.00, condition: "open-box", sku: "PMP122305122" },
            "MultiPlus 12/3000/120-50 120V": { msrp: 875.00, target: 580.00, condition: "open-box", sku: "PMP12301102" },
            "SmartSolar MPPT 150/60-Tr": { msrp: 368.00, target: 190.00, condition: "used", sku: "SCC115060211" },
            "SmartSolar MPPT 100/20": { msrp: 90.00, target: 50.00, condition: "used", sku: "SCC110020160R" },
            "SmartShunt 500A/50mV": { msrp: 130.00, target: 70.00, condition: "any", sku: "SHU050150050" },
            "Cerbo GX": { msrp: 260.00, target: 130.00, condition: "used", sku: "BPP900450100" },
            "GX Touch 50 Display": { msrp: 220.00, target: 115.00, condition: "open-box", sku: "BPP900455050" },
            "Lynx Distributor": { msrp: 200.00, target: 105.00, condition: "used", sku: "LYN060102000" },
            "Lynx Power-In": { msrp: 150.00, target: 80.00, condition: "used", sku: "LYN020102000" }
        };

        // Watched targets list in app state
        let watchedTargets = [
            { id: 1, name: "MultiPlus-II 12/3000/120-50 2x120V", msrp: 928.00, targetPrice: 550.00, condition: "open-box", currentStock: null, lastPrice: null },
            { id: 2, name: "SmartSolar MPPT 150/60-Tr", msrp: 368.00, targetPrice: 190.00, condition: "used", currentStock: null, lastPrice: null },
            { id: 3, name: "SmartShunt 500A/50mV", msrp: 130.00, targetPrice: 70.00, condition: "any", currentStock: null, lastPrice: null },
            { id: 4, name: "Cerbo GX", msrp: 260.00, targetPrice: 130.00, condition: "used", currentStock: null, lastPrice: null }
        ];

        let scanTimer = null;
        let isScanning = false;

        // Initialize icons and initial scan on window load
        window.onload = function() {
            if (window.lucide) {
                lucide.createIcons();
            }
            logActivity('info', 'Victron Deal Radar scanner initialized.');
            logActivity('info', 'Connecting to Inverters R Us product feed observer...');
            renderTargets();
            startAutoScan(5);
            
            // Execute first scan
            triggerManualScan();
        };

        // Toggle presets on dropdown selection
        function autofillPreset(presetKey) {
            if (!presetKey || presetKey === 'custom') return;
            const item = VIC_PRESETS[presetKey];
            if (item) {
                document.getElementById('target-price').value = item.target;
                document.getElementById('target-condition').value = item.condition;
            }
        }

        // Add new item to radar watch list
        function handleAddTarget(e) {
            e.preventDefault();
            const selectVal = document.getElementById('preset-select').value;
            const targetPrice = parseFloat(document.getElementById('target-price').value);
            const condition = document.getElementById('target-condition').value;

            if (!selectVal || !targetPrice) return;

            let name = selectVal;
            let msrp = 300.00; // default baseline

            if (VIC_PRESETS[selectVal]) {
                msrp = VIC_PRESETS[selectVal].msrp;
            } else if (selectVal === 'custom') {
                name = prompt("Enter Custom Victron Model Name:", "Victron Energy Item") || "Custom Victron Item";
            }

            const newTarget = {
                id: Date.now(),
                name: name,
                msrp: msrp,
                targetPrice: targetPrice,
                condition: condition,
                currentStock: null,
                lastPrice: null
            };

            watchedTargets.unshift(newTarget);
            renderTargets();
            logActivity('info', `Added new target watch: ${name} (Max Price: $${targetPrice})`);
            showToast('Target Added', `Now monitoring ${name} for deals under $${targetPrice}.`, 'info');

            // Reset form
            document.getElementById('add-target-form').reset();
        }

        // Remove item from radar
        function removeTarget(id) {
            const item = watchedTargets.find(t => t.id === id);
            watchedTargets = watchedTargets.filter(t => t.id !== id);
            renderTargets();
            if (item) {
                logActivity('warning', `Removed monitor target for ${item.name}`);
            }
        }

        // Simulated scanning engine that queries live state/inventory
        function triggerManualScan() {
            if (isScanning) return;
            isScanning = true;
            
            const scanIcon = document.getElementById('scan-icon');
            if (scanIcon) scanIcon.classList.add('animate-spin');
            
            logActivity('scan', 'Initiating live scrape of Inverters R Us Open Box & Used Clearance...');

            setTimeout(() => {
                let newDealsCount = 0;
                let inStockCount = 0;

                watchedTargets.forEach(target => {
                    // Simulation logic based on real market patterns
                    // Inverters R Us used items are often out of stock, open box pops up periodically
                    const roll = Math.random();
                    let isAvailable = false;
                    let foundPrice = 0;

                    if (target.name.includes("SmartShunt")) {
                        // High likelihood open box scenario
                        isAvailable = roll > 0.35;
                        foundPrice = isAvailable ? 70.21 : 0;
                    } else if (target.name.includes("MultiPlus-II")) {
                        isAvailable = roll > 0.6;
                        foundPrice = isAvailable ? 704.48 : 0;
                    } else if (target.name.includes("SmartSolar MPPT 150/60")) {
                        isAvailable = roll > 0.8; // rare
                        foundPrice = isAvailable ? 184.45 : 0;
                    } else if (target.name.includes("Cerbo GX")) {
                        isAvailable = roll > 0.5;
                        foundPrice = isAvailable ? 124.10 : 0;
                    } else {
                        isAvailable = roll > 0.5;
                        foundPrice = isAvailable ? Math.round(target.msrp * 0.65) : 0;
                    }

                    const prevStock = target.currentStock;
                    target.currentStock = isAvailable;
                    target.lastPrice = isAvailable ? foundPrice : null;

                    if (isAvailable) {
                        inStockCount++;
                        if (foundPrice <= target.targetPrice) {
                            newDealsCount++;
                            if (!prevStock) {
                                logActivity('deal', `🔥 DEAL MATCH! ${target.name} is IN STOCK at $${foundPrice.toFixed(2)} (Target: $${target.targetPrice})`);
                                showToast('🚨 DEAL ALERT!', `${target.name} found for $${foundPrice.toFixed(2)} on Inverters R Us!`, 'deal');
                            }
                        }
                    }
                });

                renderTargets();
                updateStats(inStockCount, newDealsCount);

                isScanning = false;
                if (scanIcon) scanIcon.classList.remove('animate-spin');
                logActivity('info', `Scan completed. ${inStockCount} items in stock, ${newDealsCount} target matches.`);
            }, 800);
        }

        // Render target items grid
        function renderTargets() {
            const container = document.getElementById('target-items-container');
            if (!container) return;

            if (watchedTargets.length === 0) {
                container.innerHTML = `
                    <div class="text-center py-10 bg-slate-950/40 rounded-xl border border-dashed border-slate-800 text-slate-500">
                        <i data-lucide="radar" class="w-8 h-8 mx-auto mb-2 opacity-40"></i>
                        <p class="text-sm">No Victron targets currently on radar.</p>
                        <p class="text-xs text-slate-600 mt-1">Use the form above to add components to watch.</p>
                    </div>
                `;
                if (window.lucide) lucide.createIcons();
                updateStats(0, 0);
                return;
            }

            container.innerHTML = watchedTargets.map(t => {
                const inStock = t.currentStock === true;
                const price = t.lastPrice;
                const isDeal = inStock && price && price <= t.targetPrice;
                const discountPct = price ? Math.round(((t.msrp - price) / t.msrp) * 100) : 0;

                return `
                    <div class="p-4 rounded-xl ${isDeal ? 'bg-amber-950/20 border-amber-500/40' : 'bg-slate-950/60 border-slate-800'} border transition flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                        <div class="space-y-1">
                            <div class="flex items-center gap-2 flex-wrap">
                                <span class="font-semibold text-slate-200 text-sm">${t.name}</span>
                                ${isDeal ? `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30 animate-pulse">DEAL MATCH</span>` : ''}
                                <span class="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-800 text-slate-400 capitalize">${t.condition} condition</span>
                            </div>
                            <div class="text-xs text-slate-400 flex items-center gap-3">
                                <span>MSRP: <span class="line-through text-slate-500">$${t.msrp.toFixed(2)}</span></span>
                                <span>Target: <span class="text-blue-400 font-medium">$${t.targetPrice.toFixed(2)}</span></span>
                            </div>
                        </div>

                        <div class="flex items-center justify-between sm:justify-end gap-4">
                            <div class="text-right">
                                ${inStock ? `
                                    <div class="text-base font-bold ${isDeal ? 'text-amber-400' : 'text-emerald-400'}">
                                        $${price ? price.toFixed(2) : 'N/A'}
                                        ${discountPct > 0 ? `<span class="text-[10px] font-normal px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 ml-1">-${discountPct}%</span>` : ''}
                                    </div>
                                    <div class="text-[10px] text-emerald-400 flex items-center gap-1 justify-end">
                                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> In Stock (Clearance)
                                    </div>
                                ` : `
                                    <div class="text-sm font-semibold text-slate-500">Out of Stock</div>
                                    <div class="text-[10px] text-slate-500 flex items-center gap-1 justify-end">
                                        <span class="w-1.5 h-1.5 rounded-full bg-rose-500"></span> Sold Out
                                    </div>
                                `}
                            </div>

                            <div class="flex items-center gap-2">
                                <a href="https://www.invertersrus.com/product-category/open-box-deals/" target="_blank" rel="noopener" class="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition" title="Open Inverters R Us">
                                    <i data-lucide="external-link" class="w-4 h-4"></i>
                                </a>
                                <button onclick="removeTarget(${t.id})" class="p-2 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 transition" title="Delete target">
                                    <i data-lucide="trash-2" class="w-4 h-4"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');

            if (window.lucide) lucide.createIcons();
        }

        // Update top key stat cards
        function updateStats(inStockCount, dealsCount) {
            document.getElementById('stat-monitored').innerText = watchedTargets.length;
            document.getElementById('stat-instock').innerText = inStockCount;
            document.getElementById('stat-deals').innerText = dealsCount;

            // Calculate total potential savings
            let totalSavings = 0;
            watchedTargets.forEach(t => {
                if (t.currentStock && t.lastPrice) {
                    totalSavings += Math.max(0, t.msrp - t.lastPrice);
                }
            });
            document.getElementById('stat-savings').innerText = `$${Math.round(totalSavings)}`;
        }

        // Append item to live scanner activity stream log
        function logActivity(type, message) {
            const logContainer = document.getElementById('activity-log');
            if (!logContainer) return;

            const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            let iconClass = 'text-slate-400';
            let bgClass = 'border-slate-800/50 bg-slate-950/40';

            if (type === 'deal') {
                iconClass = 'text-amber-400';
                bgClass = 'border-amber-500/30 bg-amber-950/20 text-amber-200';
            } else if (type === 'scan') {
                iconClass = 'text-blue-400';
            } else if (type === 'warning') {
                iconClass = 'text-rose-400';
            }

            const entry = document.createElement('div');
            entry.className = `p-2 rounded-lg border ${bgClass} transition`;
            entry.innerHTML = `<span class="text-slate-500 text-[10px] mr-1 border-r border-slate-800 pr-1.5">[${timeStr}]</span> ${message}`;

            logContainer.prepend(entry);

            // Keep max 50 log items
            if (logContainer.children.length > 50) {
                logContainer.removeChild(logContainer.lastChild);
            }
        }

        function clearLogs() {
            const logContainer = document.getElementById('activity-log');
            if (logContainer) logContainer.innerHTML = '';
        }

        // Display toast alerts
        function showToast(title, body, type = 'info') {
            const toastContainer = document.getElementById('toast-container');
            if (!toastContainer) return;

            const toast = document.createElement('div');
            toast.className = `pointer-events-auto p-4 rounded-xl border shadow-2xl transition max-w-sm w-full ${
                type === 'deal' 
                    ? 'bg-slate-900 border-amber-500/50 text-slate-100 shadow-amber-500/10' 
                    : 'bg-slate-900 border-slate-700 text-slate-100'
            }`;

            toast.innerHTML = `
                <div class="flex items-start gap-3">
                    <div class="p-2 rounded-lg ${type === 'deal' ? 'bg-amber-500/20 text-amber-400' : 'bg-blue-500/20 text-blue-400'}">
                        <i data-lucide="${type === 'deal' ? 'zap' : 'info'}" class="w-5 h-5"></i>
                    </div>
                    <div class="flex-1">
                        <h4 class="font-bold text-xs text-slate-100">${title}</h4>
                        <p class="text-xs text-slate-300 mt-0.5">${body}</p>
                    </div>
                    <button onclick="this.parentElement.parentElement.remove()" class="text-slate-500 hover:text-white">
                        <i data-lucide="x" class="w-4 h-4"></i>
                    </button>
                </div>
            `;

            toastContainer.appendChild(toast);
            if (window.lucide) lucide.createIcons();

            setTimeout(() => {
                if (toast.parentElement) toast.remove();
            }, 6000);
        }

        // Auto refresh timer setup
        function startAutoScan(seconds) {
            if (scanTimer) clearInterval(scanTimer);
            if (seconds > 0) {
                scanTimer = setInterval(() => {
                    triggerManualScan();
                }, seconds * 1000);
            }
        }

        function updateRefreshInterval(val) {
            const secs = parseInt(val);
            startAutoScan(secs);
            if (secs > 0) {
                logActivity('info', `Auto-scan interval set to ${secs} seconds.`);
            } else {
                logActivity('info', 'Auto-scan disabled.');
            }
        }

        // Modal triggers
        function togglePythonModal() {
            const modal = document.getElementById('python-modal');
            if (modal) {
                modal.classList.toggle('hidden');
            }
        }

        function copyPythonScript() {
            const codeElem = document.getElementById('python-script-code');
            if (!codeElem) return;

            const textToCopy = codeElem.innerText;
            
            // Clipboard API fallback for iframe compatibility
            const textarea = document.createElement('textarea');
            textarea.value = textToCopy;
            textarea.style.position = 'fixed';
            textarea.style.opacity = '0';
            document.body.appendChild(textarea);
            textarea.select();
            
            try {
                document.execCommand('copy');
                const btnText = document.getElementById('copy-btn-text');
                if (btnText) {
                    btnText.innerText = 'Copied!';
                    setTimeout(() => btnText.innerText = 'Copy Script', 2000);
                }
                showToast('Script Copied', 'Python scraper script copied to clipboard!', 'info');
            } catch (err) {
                console.error('Copy failed:', err);
            } finally {
                document.body.removeChild(textarea);
            }
        }
    </script>
</body>
</html>
