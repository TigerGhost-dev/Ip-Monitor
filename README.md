# 🔐 Tor IP Monitor

A Linux desktop application that monitors your network in real time to ensure your traffic is securely routed through Tor.

It detects IP changes, verifies Tor connectivity, checks for DNS leaks, and alerts you instantly if your anonymity is compromised.

---

## 🚀 Features

* 🌐 Real-time public IP monitoring
* 🧅 Tor connection detection
* 🔥 DNS leak detection (advanced)
* 🔐 Kill-switch to block traffic when unsafe
* 🔔 Desktop notifications on status changes
* 🖥️ Hacker-style GUI with live updates
* 📊 Logging of all IP and status changes

---

## 🧠 How It Works

The application monitors three key things:

* **Real IP** → Your actual network IP
* **Tor IP** → IP routed through Tor (via proxychains)
* **DNS behavior** → Detects if DNS queries leak outside Tor

It determines whether your connection is:

* 🟢 **SAFE** → Tor active, Firefox running, no leaks
* 🔴 **UNSAFE** → Tor down, Firefox closed, or DNS leak detected

---

## ⚙️ Requirements

* Linux (tested on Ubuntu/Debian)
* Python 3
* Tor
* proxychains
* dnsutils

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/tor-ip-monitor.git
cd tor-ip-monitor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ▶️ Usage

Start Tor:

```bash
sudo systemctl start tor
```

Run the application:

```bash
python main.py
```

---

## 🌐 Using with Firefox

Run Firefox through Tor:

```bash
proxychains firefox
```

---

## ⚠️ Kill-Switch Warning

If the app detects an unsafe state, it blocks all outgoing traffic using `iptables`.

To restore internet manually:

```bash
sudo iptables -P OUTPUT ACCEPT
```

---

## 📊 Logs

All events are stored in:

```
logs.txt
```

---

## ⚠️ Disclaimer

This tool is for **monitoring purposes only** and does not guarantee complete anonymity.

Users should still follow best practices when using Tor.

---

## 🛠️ Future Improvements

* System tray minimization
* Animated background (globe)
* Live IP history graph
* Packaging as a `.deb` installer

---
