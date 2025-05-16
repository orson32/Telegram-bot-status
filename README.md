<p align="center">
  <img src="https://github.com/orson32/telegram-bot-status/blob/main/A_2D_digital_graphic_design_image_displays_release.png?raw=true" alt="Bot Status Banner">
</p>


# Telegram Bot para Monitoreo de Raspberry Pi

Este bot de Telegram te permite monitorear tu Raspberry Pi en tiempo real, desde cualquier lugar, y recibir alertas cuando algo va mal.

---

## Características

- 📊 `/status`: Estado general (CPU, RAM, temperatura)
- ⏱️ `/uptime`: Tiempo encendida
- 🌐 `/ip`: Dirección IP local
- 💽 `/disk`: Uso del disco
- 🐳 `/docker`: Contenedores Docker activos
- 🔧 `/services`: Estado de servicios clave (`docker`, `nginx`, `glances`)
- ♻️ `/reboot`: Reinicia la Raspberry Pi (usa con cuidado)

---

## Alertas Automáticas (cada 5 min)

- 🌡️ Temperatura > 70 °C
- 🧠 RAM > 90%
- 💽 Disco casi lleno (> 90%)
- ❌ Servicios caídos

---

## Requisitos

- Raspberry Pi con Docker y Docker Compose instalados
- `vcgencmd` habilitado (normal en Raspbian)
- Un bot de Telegram creado vía [@BotFather](https://t.me/BotFather)

---

## Cómo usar

1. Clona el repositorio:

```bash
git clone https://github.com/orson32/Telegram-bot-status.git
cd Telegram-bot-status
