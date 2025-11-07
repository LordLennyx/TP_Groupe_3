#!/usr/bin/env python3
import os
import sys
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText

# --- CONFIG GEMINI ---
# tu peux aussi faire: api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

# --- CONFIG EMAILS ---
EMAILS = {
    "LordLennyx": "lensdaniels237@gmail.com",
    "Delbrique": "valentinbiyong2@gmail.com",
}

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "valentinbiyong2@gmail.com"
SMTP_PASS = "wszs wlbw iqfx aqlx"

def validate_ts(code: str, author: str, filename: str) -> str:
    prompt = f"""
Tu es un expert TypeScript strict. Vérifie ce code dans {filename} :
{code}

RÈGLES OBLIGATOIRES :
1. Types explicites partout (interdit : any)
2. Pas de console.log(), alert(), debugger
3. Variables en camelCase
4. Interfaces bien définies
5. Pas de variables globales non déclarées
6. Code propre et commenté si complexe
Auteur : {author}

Retourne UNIQUEMENT :
- "VALIDE"
- "INVALIDE: [explication courte]"
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"ERREUR API: {e}"

def send_rejection_email(author: str, filename: str, reason: str):
    recipient = EMAILS.get(author, "fallback@example.com")
    subject = f"Commit refusé : {filename}"
    body = f"""Bonjour {author},

Ton commit a été refusé par Gemini.
Fichier : {filename}
Raison : {reason}

Corrige et recommence.
"""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = recipient

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        print("Email de refus envoyé.")
    except Exception as e:
        print(f"Échec email : {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 validate_commit.py <fichier_ts> <auteur>")
        sys.exit(1)

    filename = sys.argv[1]
    author = sys.argv[2]

    if not os.path.exists(filename):
        print(f"FICHIER {filename} INTROUVABLE")
        sys.exit(1)

    with open(filename, "r", encoding="utf-8") as f:
        code = f.read()

    result = validate_ts(code, author, filename)
    print("Résultat modèle :", result)

    if result.startswith("VALIDE"):
        print("✅ COMMIT VALIDÉ PAR GEMINI")
        sys.exit(0)
    else:
        # enlever le "INVALIDE: " si présent
        reason = result
        if result.startswith("INVALIDE:"):
            reason = result[len("INVALIDE:"):].strip()
        send_rejection_email(author, filename, reason)
        print("❌ COMMIT REFUSÉ PAR GEMINI")
        sys.exit(1)

if __name__ == "__main__":
    main()
