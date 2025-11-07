#!/usr/bin/env python3
import os
import sys
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText

# === CONFIGURATION GEMINI ===
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"  # modèle à jour

# === EMAILS ===
EMAILS = {
    "LordLennyx": "lensdaniels237@gmail.com",
    "Delbrique": "valentinbiyong2@gmail.com",
}

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "valentinbiyong2@gmail.com"
SMTP_PASS = "wszswlbwiqfxaqlx"  # mot de passe d’application Gmail

def validate_ts(code: str, author: str, filename: str) -> str:
    prompt = f"""
Tu es un expert TypeScript strict.
Vérifie ce code dans {filename} :
{code}

RÈGLES OBLIGATOIRES :
1. Types explicites (pas de 'any')
2. Pas de console.log(), alert(), debugger
3. Variables en camelCase
4. Interfaces bien définies
5. Pas de variables globales non déclarées
Auteur : {author}

Retourne UNIQUEMENT :
- "VALIDE"
- "INVALIDE: [explication courte]"
"""
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        resp = model.generate_content(prompt)
        return resp.text.strip()
    except Exception as e:
        return f"ERREUR API: {e}"

def send_rejection_email(author: str, filename: str, reason: str):
    recipient = EMAILS.get(author, "fallback@example.com")
    subject = f"🚨 Commit refusé : {filename}"
    body = f"""
Bonjour {author},

Ton commit a été refusé par l'IA Gemini.
Fichier : {filename}
Raison : {reason}

Corrige et recommence ton commit.
— TP_Groupe_3
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
        print(f"📨 Email envoyé à {author} ({recipient})")
    except Exception as e:
        print(f"❌ Échec envoi email : {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python validate_commit.py <fichier> <auteur>")
        sys.exit(1)

    filename = sys.argv[1]
    author = sys.argv[2]

    if not os.path.exists(filename):
        print(f"⚠️ FICHIER {filename} INTROUVABLE")
        sys.exit(1)

    with open(filename, "r", encoding="utf-8") as f:
        code = f.read()

    result = validate_ts(code, author, filename)
    print(result)

    # 🔴 si erreur API ou invalide → commit refusé
    if result.startswith("ERREUR API:") or result.startswith("INVALIDE"):
        send_rejection_email(author, filename, result)
        print("❌ COMMIT REFUSÉ PAR GEMINI")
        sys.exit(1)
    else:
        print("✅ VALIDÉ PAR GEMINI")
        sys.exit(0)
