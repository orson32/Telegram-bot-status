import telebot
from telebot.types import BotCommand
import psutil
import subprocess
import os
import socket
import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID_AUTORIZADO = int(os.getenv("CHAT_ID"))

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

def set_command_menu():
    bot.set_my_commands([
        BotCommand("status", "📊 Ver estado de la Raspberry"),
        BotCommand("uptime", "⏱️ Tiempo encendida"),
        BotCommand("ip", "🌐 Ver IP local"),
        BotCommand("disk", "💽 Uso de disco"),
        BotCommand("docker", "🐳 Contenedores activos"),
        BotCommand("services", "🔧 Estado de servicios"),
        BotCommand("reboot", "♻️ Reiniciar Raspberry Pi")
    ])

set_command_menu()

def get_temp():
    out = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
    return out.strip().replace("temp=", "")

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    return str(datetime.timedelta(seconds=int(uptime_seconds)))

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "❌ No IP"

def get_disk_usage():
    usage = psutil.disk_usage("/")
    return f"{usage.percent}% used of {round(usage.total / (1024**3), 1)}GB"

def get_docker_containers():
    try:
        out = subprocess.check_output(["docker", "ps", "--format", "{{.Names}}: {{.Status}}"])
        return out.decode().strip() or "🚫 No running containers"
    except Exception as e:
        return f"❌ Docker error: {str(e)}"

def get_services_status():
    services = ["docker", "nginx", "glances"]
    status_list = []
    for service in services:
        try:
            out = subprocess.check_output(["systemctl", "is-active", service]).decode().strip()
            icon = "✅" if out == "active" else "❌"
            status_list.append(f"{icon} {service}")
        except:
            status_list.append(f"❓ {service} (not found)")
    return "\n".join(status_list)

@bot.message_handler(commands=["status"])
def status(message):
    if message.chat.id != CHAT_ID_AUTORIZADO:
        return
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    temp = get_temp()
    clean_temp = ''.join(filter(lambda c: c.isdigit() or c == '.', temp))

    msg = (
        "📊 *Raspberry Pi Status*\n"
        f"`CPU:` {cpu}%  {'🔥' if cpu > 80 else '✅'}\n"
        f"`RAM:` {ram}%  {'🧠⚠️' if ram > 80 else '✅'}\n"
        f"`Temp:` {temp}  {'🌡️🔥' if float(clean_temp) > 70 else '❄️'}"
    )
    bot.reply_to(message, msg)

@bot.message_handler(commands=["uptime"])
def uptime(message):
    if message.chat.id != CHAT_ID_AUTORIZADO:
        return
    bot.reply_to(message, f"⏱️ *Uptime:* `{get_uptime()}`")

@bot.message_handler(commands=["ip"])
def ip(message):
    if message.chat.id != CHAT_ID_AUTORIZADO:
        return
    bot.reply_to(message, f"🌐 *IP:* `{get_ip()}`")

@bot.message_handler(commands=["reboot"])
def reboot(message):
    if message.chat.id != CHAT_ID_AUTORIZADO:
        return
    bot.reply_to(message, "♻️ *Reiniciando Raspberry Pi...*")
    subprocess.call(["reboot"])

@bot.message_handler(commands=["disk"])
def disk(message):
    if message.chat.id != CHAT_ID_AUTORIZADO:
        return
    usage = get_disk_usage()
    bot.reply_to(message, f"💽 *Disco:* `{usage}`")

@bot.message_handler(commands=["docker"])
def docker_status(message):
    if message.chat.id != CHAT_ID_AUTORIZADO:
        return
    containers = get_docker_containers()
    bot.reply_to(message, f"🐳 *Contenedores activos:*\n```{containers}```")

@bot.message_handler(commands=["services"])
def services_status(message):
    if message.chat.id != CHAT_ID_AUTORIZADO:
        return
    statuses = get_services_status()
    bot.reply_to(message, f"🔧 *Servicios:* \n```{statuses}```")

bot.polling()
