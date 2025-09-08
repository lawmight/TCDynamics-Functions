import logging
import os
import smtplib
import json
from email.message import EmailMessage
import azure.functions as func

SMTP_HOST = "smtp.zoho.com"
SMTP_PORT = 587
SMTP_USER = os.environ["SMTP_USER"]
SMTP_PASS = os.environ["SMTP_PASS"]

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
        
        # Extract WorkFlowAI specific fields
        company_name = data.get("company_name", "").strip()
        contact_name = data.get("contact_name", data.get("name", "")).strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        company_size = data.get("company_size", "").strip()
        industry = data.get("industry", "").strip()
        location = data.get("location", "").strip()
        message = data.get("message", "").strip()
        budget_range = data.get("budget_range", "").strip()
        timeline = data.get("timeline", "").strip()

        # Validate required fields
        if not contact_name or not email or not company_name:
            return func.HttpResponse(
                json.dumps({
                    "success": False,
                    "message": "Nom, email et nom de l'entreprise sont requis pour WorkFlowAI."
                }),
                status_code=400,
                mimetype="application/json"
            )

        # Create enhanced email for WorkFlowAI
        msg = EmailMessage()
        msg["Subject"] = f"🚀 WorkFlowAI - NOUVELLE DEMANDE COMMERCIALE - {company_name}"
        msg["From"] = SMTP_USER
        msg["To"] = SMTP_USER  # Send to yourself
        
        # Enhanced email body for business inquiries
        email_body = f"""🚀 NOUVELLE DEMANDE COMMERCIALE - WorkFlowAI

📊 INFORMATIONS ENTREPRISE:
• Entreprise: {company_name}
• Contact: {contact_name}
• Email: {email}
• Téléphone: {phone or 'Non fourni'}
• Taille: {company_size or 'Non spécifiée'}
• Secteur: {industry or 'Non spécifié'}
• Localisation: {location or 'Non spécifiée'}

💰 INFORMATIONS COMMERCIALES:
• Budget: {budget_range or 'Non spécifié'}
• Délai: {timeline or 'Non spécifié'}

💬 MESSAGE:
{message}

📍 CIBLE: Entreprises de Montigny-le-Bretonneux et Guyancourt
🎯 SERVICE: Automatisation IA pour entreprises
⏰ PRIORITÉ: HAUTE - Répondre dans les 24h

---
Envoyé automatiquement depuis le formulaire WorkFlowAI."""

        msg.set_content(email_body)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        return func.HttpResponse(
            json.dumps({
                "success": True,
                "message": "Merci pour votre intérêt pour WorkFlowAI ! Notre équipe commerciale vous contactera dans les 24h pour discuter de l'automatisation de votre entreprise."
            }),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"WorkFlowAI contact form error: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "success": False,
                "message": "Une erreur s'est produite. Veuillez réessayer ou nous contacter directement."
            }),
            status_code=500,
            mimetype="application/json"
        )
