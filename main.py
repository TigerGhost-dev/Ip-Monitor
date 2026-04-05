import requests
import time

def get_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return None

def is_tor(ip):
    try:
        res = requests.get(f"https://check.torproject.org/api/ip?ip={ip}").json()
        return res.get("IsTor", False)
    except:
        return False

last_ip = None

while True:
    ip = get_ip()

    if ip:
        tor = is_tor(ip)

        if ip != last_ip:
            print(f"[!] IP Changed: {ip}")

        if tor:
            print(f"[SAFE] Using Tor: {ip}")
        else:
            print(f"[UNSAFE] Real IP: {ip}")

        last_ip = ip
    else:
        print("[ERROR] Could not fetch IP")

    time.sleep(5)