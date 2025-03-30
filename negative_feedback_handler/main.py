from fastapi import FastAPI
import os
import json
import requests

app = FastAPI()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = "no-reply@yourdomain.com"
SUPPORT_EMAIL = "support@yourcompany.com"

def send_email(to_email, subject, content):
    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": SENDER_EMAIL},
        "subject": subject,
        "content": [{"type": "text/plain", "value": content}]
    }
    requests.post(url, headers=headers, json=data)

@app.post("/handle_negative_feedback/")
async def handle_negative_feedback(feedback: dict):
    feedback_id = feedback["feedback_id"]
    sentiment = feedback["sentiment"]
    user_email = feedback.get("user_email", SUPPORT_EMAIL)

    if sentiment.lower() == "négatif":
        send_email(SUPPORT_EMAIL, "Alerte : Client insatisfait", f"Feedback {feedback_id} négatif.")
        send_email(user_email, "Nous sommes désolés", f"Bonjour, nous avons bien reçu votre feedback {feedback_id}. Nous allons vous contacter.")

    return {"status": "processed", "feedback_id": feedback_id}
