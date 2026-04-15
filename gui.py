import tkinter as tk

class MonitorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tor IP Monitor")
        self.root.geometry("520x420")
        self.root.resizable(False, False)

        # Colors
        self.bg_dark = "#0d1117"
        self.green = "#00ff00"
        self.red = "#ff3333"
        self.white = "#ffffff"

        self.root.configure(bg=self.bg_dark)

        # Blink control
        self.blinking = False
        self.blink_state = False

        # ===== STATUS =====
        self.status_label = tk.Label(
            self.root,
            text="INITIALIZING",
            font=("Courier", 30, "bold"),
            fg=self.green,
            bg=self.bg_dark
        )
        self.status_label.pack(pady=15)

        # ===== IP DISPLAY =====
        self.real_ip = tk.Label(
            self.root,
            font=("Courier", 16, "bold"),
            fg=self.white,
            bg=self.bg_dark
        )
        self.real_ip.pack(pady=5)

        self.tor_ip = tk.Label(
            self.root,
            font=("Courier", 16, "bold"),
            fg=self.green,
            bg=self.bg_dark
        )
        self.tor_ip.pack(pady=5)

        # ===== FIREFOX =====
        self.firefox = tk.Label(
            self.root,
            font=("Courier", 13),
            fg=self.white,
            bg=self.bg_dark
        )
        self.firefox.pack(pady=5)

        # ===== TOR STATUS =====
        self.tor_status = tk.Label(
            self.root,
            font=("Courier", 13, "bold"),
            fg=self.white,
            bg=self.bg_dark
        )
        self.tor_status.pack(pady=10)

        # ===== DNS STATUS =====
        self.dns_status = tk.Label(
            self.root,
            font=("Courier", 13, "bold"),
            fg=self.white,
            bg=self.bg_dark,
            wraplength=480,
            justify="center"
        )
        self.dns_status.pack(pady=10)

    # =========================
    # UPDATE UI
    # =========================
    def update(self, real_ip, tor_ip, firefox_running, status, dns_leak, dns_ip, tor_dns_ip):

        # IP display
        self.real_ip.config(text=f"Real IP: {real_ip}")
        self.tor_ip.config(text=f"Tor IP: {tor_ip}")

        # Firefox status
        self.firefox.config(
            text="Firefox: RUNNING" if firefox_running else "Firefox: NOT RUNNING"
        )

        # DNS display
        if dns_leak:
            self.dns_status.config(
                text=f"DNS LEAK DETECTED 🔴\nSystem DNS: {dns_ip}",
                fg=self.red
            )
        else:
            self.dns_status.config(
                text=f"DNS SAFE 🟢\nTor DNS: {tor_dns_ip}",
                fg=self.green
            )

        # Status switching
        if status == "SAFE":
            self.set_safe()
        else:
            self.set_unsafe()

    # =========================
    # SAFE STATE
    # =========================
    def set_safe(self):
        self.blinking = False  # stop blinking

        self.root.configure(bg=self.bg_dark)

        self.status_label.config(
            text="SAFE",
            fg=self.green,
            bg=self.bg_dark
        )

        self.tor_status.config(
            text="Tor: CONNECTED 🟢",
            fg=self.green,
            bg=self.bg_dark
        )

    # =========================
    # UNSAFE STATE
    # =========================
    def set_unsafe(self):
        self.tor_status.config(
            text="Tor: NOT SECURE 🔴",
            fg=self.red,
            bg=self.bg_dark
        )

        if not self.blinking:
            self.blinking = True
            self.blink_red()

    # =========================
    # BLINK EFFECT
    # =========================
    def blink_red(self):
        if not self.blinking:
            return

        self.blink_state = not self.blink_state

        bg_color = self.red if self.blink_state else self.bg_dark

        self.root.configure(bg=bg_color)

        self.status_label.config(
            text="UNSAFE",
            fg=self.white,
            bg=bg_color
        )

        self.root.after(500, self.blink_red)

    # =========================
    # RUN GUI
    # =========================
    def run(self):
        self.root.mainloop()