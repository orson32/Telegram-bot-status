# Telegram Bot para Monitoreo de Raspberry Pi

Este bot de Telegram te permite monitorear el estado de tu Raspberry Pi en tiempo real, consultar datos como CPU, RAM, temperatura, uptime, y también recibir alertas automáticas si algo se sale de control. Todo empaquetado en un contenedor Docker listo para producción.

## Características

- 📊 `/status`: Muestra CPU, RAM y temperatura
- ⏱️ `/uptime`: Muestra cuánto tiempo lleva encendida la Raspberry
- 🌐 `/ip`: Muestra la IP local de la Raspberry
- 💽 `/disk`: Muestra el uso del disco
- 🐳 `/docker`: Muestra contenedores Docker activos
- 🔧 `/services`: Muestra el estado de servicios clave (`docker`, `nginx`, `glances`)
- ♻️ `/reboot`: Reinicia la Raspberry Pi (usarlo con responsabilidad)
- 🚨 Alertas automáticas cada 5 min si:
  - Temperatura > 70 °C
  - RAM > 90%
  - Disco casi lleno (> 90%)
  - Servicios caídos

## Requisitos

- Docker y Docker Compose instalados
- Python 3.11 o superior (solo dentro del contenedor)
- Una Raspberry Pi con `vcgencmd` habilitado

## Cómo usar

1. Clona el repositorio:

```bash
git clone https://github.com/orson32/Telegram-bot-status.git
cd Telegram-bot-status
```

2. Abre y edita `docker-compose.yml`:
   - Sustituye `BOT_TOKEN` con el token de tu bot de Telegram
   - Sustituye `CHAT_ID` con tu ID de usuario de Telegram

3. Construye y arranca el bot:

```bash
docker compose up -d --build
```

4. Escribe `/status` en Telegram y empieza a monitorear tu Raspberry como un pro.

## Autor

Creado por [@orson32](https://github.com/orson32) — orgullosamente hackeado sobre una Raspberry Pi.

