import logging
import os
import smtplib
from email.message import EmailMessage
import azure.functions as func

SMTP_HOST = "smtp.zoho.com"
SMTP_PORT = 587
SMTP_USER = os.environ["SMTP_USER"]
SMTP_PASS = os.environ["SMTP_PASS"]

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not name or not email or not message:
            return func.HttpResponse("Champs manquants", status_code=400)

        msg = EmailMessage()
        msg["Subject"] = f"Nouveau message de {name}"
        msg["From"] = SMTP_USER
        msg["To"] = "contact@tcdynamics.fr"
        msg.set_content(f"De : {name} <{email}>\n\n{message}")

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        return func.HttpResponse("Message envoyé !", status_code=200)
    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse("Erreur serveur", status_code=500)
