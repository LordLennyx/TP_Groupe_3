#!/usr/bin/env python3
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText

API_KEY = "AIzaSyDZXeR1JVQHrv7tYWpJ1GWcSyNNxFn7KzQ"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")

EMAILS = {
    "LordLennyx": "lensdaniels237@gmail.com",
    "Delbrique": "valentinbiyong2@gmail.com"
}

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "valentinbiyong2@gmail.com"
SMTP_PASS = "wszswlbwiqfxaqlx"

def validate_ts(code: str, author: str, filename: str):
    prompt = f"""
Tu es un relecteur TypeScript très strict.
Analyse le code suivant du fichier {filename} écrit par {author}.

Code:
{code}

Règles:
1. pas de any
2. pas de console.log / alert / debugger
3. types explicites
4. nommage camelCase
5. expliquer quoi corriger

Réponds exactement dans ce format:
STATUS: VALIDE ou INVALIDE
MESSAGE: phrase(s) à envoyer à l'auteur, en français, qui expliquent ce qu'il doit corriger.
"""
    try:
        resp = model.generate_content(prompt)
        txt = resp.text.strip()
        status = "ERREUR"
        message = txt
        for line in txt.splitlines():
            if line.startswith("STATUS:"):
                status = line.replace("STATUS:", "").strip()
            if line.startswith("MESSAGE:"):
                message = line.replace("MESSAGE:", "").strip()
        return status, message
    except Exception as e:
        return "ERREUR", f"ERREUR API: {e}"

def send_rejection_email(author: str, filename: str, msg_text: str):
    recipient = EMAILS.get(author, "fallback@example.com")
    subject = f"Commit refusé : {filename}"
    body = f"Bonjour {author},\n\n{msg_text}\n\nCorrige et recommence.\nTP_Groupe_3"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = recipient
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, recipient, msg.as_string())
        server.quit()
        print("Email envoyé.")
    except Exception as e:
        print(f"Échec email : {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python3 validate_commit.py <fichier> <auteur>")
        raise SystemExit(1)
    filename, author = sys.argv[1], sys.argv[2]
    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
        status, message = validate_ts(code, author, filename)
        print("STATUS:", status)
        print("MESSAGE:", message)
        if status.upper().startswith("INVALIDE") or status.upper().startswith("ERREUR"):
            send_rejection_email(author, filename, message)
            print("❌ COMMIT REFUSÉ PAR GEMINI")
            raise SystemExit(1)
        else:
            print("✅ VALIDÉ PAR GEMINI")
            raise SystemExit(0)
    except FileNotFoundError:
        print(f"FICHIER {filename} INTROUVABLE")
        raise SystemExit(1)
