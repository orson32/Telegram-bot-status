import telebot
import psutil
import subprocess
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

def send_alert(msg):
    bot.send_message(CHAT_ID, f"🚨 *Alerta Raspberry Pi:*\n{msg}")

def check_temp():
    try:
        out = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
        clean = ''.join(c for c in out if c.isdigit() or c == '.')
        return float(clean)
    except:
        return 0

def check_ram():
    return psutil.virtual_memory().percent

def check_disk():
    usage = psutil.disk_usage("/")
    return usage.percent

def check_services():
    failed = []
    for svc in ["docker", "nginx", "glances"]:
        try:
            state = subprocess.check_output(["systemctl", "is-active", svc]).decode().strip()
            if state != "active":
                failed.append(svc)
        except:
            failed.append(svc)
    return failed

# Lógica de alertas
alerts = []

if check_temp() > 70:
    alerts.append("🌡️ Temperatura alta")

if check_ram() > 90:
    alerts.append("🧠 RAM > 90%")

if check_disk() > 90:
    alerts.append("💽 Disco casi lleno")

services = check_services()
if services:
    alerts.append("🔧 Servicios caídos: " + ", ".join(services))

if alerts:
    send_alert("\n".join(alerts))
