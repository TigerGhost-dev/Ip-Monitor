import threading
import time
import requests
import subprocess
import os
from datetime import datetime

from gui import MonitorGUI

# =========================
# NETWORK FUNCTIONS
# =========================

def get_real_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Error"

def get_tor_ip():
    try:
        result = subprocess.check_output(
            ["proxychains", "curl", "-s", "https://api.ipify.org"]
        )
        return result.decode().strip()
    except:
        return "Not Connected"

def is_firefox_running():
    try:
        subprocess.check_output(["pgrep", "firefox"])
        return True
    except:
        return False

# =========================
# REAL DNS LEAK TEST
# =========================

def get_dns_ip():
    try:
        result = subprocess.check_output(
            ["dig", "+short", "myip.opendns.com", "@resolver1.opendns.com"]
        )
        return result.decode().strip()
    except:
        return "Unknown"

def get_tor_dns_ip():
    try:
        result = subprocess.check_output(
            ["proxychains", "dig", "+short", "myip.opendns.com", "@resolver1.opendns.com"]
        )
        return result.decode().strip()
    except:
        return "Unknown"

def check_dns_leak(real_ip, tor_ip):
    dns_ip = get_dns_ip()
    tor_dns_ip = get_tor_dns_ip()

    # Leak if Tor DNS resolves to real IP
    if tor_dns_ip == real_ip:
        return True, dns_ip, tor_dns_ip

    return False, dns_ip, tor_dns_ip

# =========================
# LOGGING
# =========================

def log_event(real_ip, tor_ip, status):
    with open("logs.txt", "a") as f:
        f.write(f"{datetime.now()} | REAL: {real_ip} | TOR: {tor_ip} | {status}\n")

# =========================
# NOTIFICATIONS
# =========================

def notify(title, msg):
    os.system(f'notify-send "{title}" "{msg}"')

# =========================
# KILL SWITCH
# =========================

killswitch_active = False

def enable_killswitch():
    global killswitch_active
    if not killswitch_active:
        os.system("iptables -P OUTPUT DROP")
        killswitch_active = True

def disable_killswitch():
    global killswitch_active
    if killswitch_active:
        os.system("iptables -P OUTPUT ACCEPT")
        killswitch_active = False

# =========================
# MONITOR LOOP
# =========================

last_status = None

def monitor(gui):
    global last_status

    while True:
        real_ip = get_real_ip()
        tor_ip = get_tor_ip()
        firefox_running = is_firefox_running()

        tor_connected = tor_ip != "Not Connected" and tor_ip != real_ip

        dns_leak, dns_ip, tor_dns_ip = check_dns_leak(real_ip, tor_ip)

        if tor_connected and firefox_running and not dns_leak:
            status = "SAFE"
        else:
            status = "UNSAFE"

        gui.update(
            real_ip,
            tor_ip,
            firefox_running,
            status,
            dns_leak,
            dns_ip,
            tor_dns_ip
        )

        log_event(real_ip, tor_ip, status)

        # Kill-switch
        if status == "UNSAFE":
            enable_killswitch()
        else:
            disable_killswitch()

        # Notifications
        if last_status and last_status != status:
            if status == "UNSAFE":
                notify("WARNING 🔴", f"Leak or exposure detected!")
            else:
                notify("SAFE 🟢", f"Tor fully secured")

        last_status = status

        time.sleep(5)

# =========================
# START APP
# =========================

gui = MonitorGUI()

thread = threading.Thread(target=monitor, args=(gui,))
thread.daemon = True
thread.start()

gui.run()