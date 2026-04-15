import pystray
from PIL import Image, ImageDraw
import threading

def create_icon():
    image = Image.new("RGB", (64, 64), "black")
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill="green")
    return image

def run_tray(on_quit):
    icon = pystray.Icon("Tor Monitor", create_icon(), "Tor Monitor")

    def quit_app(icon, item):
        icon.stop()
        on_quit()

    icon.menu = pystray.Menu(
        pystray.MenuItem("Quit", quit_app)
    )

    threading.Thread(target=icon.run).start()