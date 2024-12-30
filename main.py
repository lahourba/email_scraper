import os
import re
import openai
from gmail_auth import gmail_authenticate
from read_emails import get_emails_from_label

openai.api_key = os.getenv("OPENAI_API_KEY")  # Récupère la clé depuis la variable d'env


def format_bold_text(text):
    """
    Remplace les `**texte**` par `<strong>texte</strong>` pour le HTML.
    """
    return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

def convert_bullets_to_html(text):
    # Remplace chaque ligne commençant par un tiret suivi d'un espace par un élément <li>
    lines = text.splitlines()
    html_list = ""
    in_list = False

    for line in lines:
        # Applique la mise en forme du texte en gras
        line = format_bold_text(line)

        if line.startswith("- "):  # Détecte les puces
            if not in_list:
                html_list += "<ul>\n"
                in_list = True
            html_list += f"  <li>{line[2:].strip()}</li>\n"
        else:
            if in_list:
                html_list += "</ul>\n"
                in_list = False
            html_list += f"<p>{line.strip()}</p>\n"

    # Ferme la liste si elle est encore ouverte
    if in_list:
        html_list += "</ul>\n"

    return html_list

# Fonction pour formatter le résumé en HTML
def format_summary_as_html(summaries):
    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; padding: 0; }
            h1 { color: #333; text-align: center; }
            h2 { color: #555; margin-top: 20px; }
            p { margin: 10px 0; text-align: justify; }
            hr { border: none; border-top: 1px solid #ccc; margin: 20px 0; }
            .summary { margin-bottom: 30px; padding: 15px; background-color: #f9f9f9; border-radius: 8px; }
            .summary h2 { margin-top: 0; }
        </style>
    </head>
    <body>
        <h1>Résumé des newsletters</h1>
    """
    for i, (subject, summary) in enumerate(summaries, start=1):
        html += f"""
        <div class="summary">
            <h2>Résumé de la newsletter {i} : {subject}</h2>
            <p>{summary}</p>
        </div>
        """
    html += """
    </body>
    </html>
    """
    return html

def summarize_email_with_chat(email):
    messages = [
        {"role": "system", "content": "Tu es un assistant chargé de résumer des newsletters."},
        {"role": "user", "content": (
            f"Voici une newsletter à résumer en français, en quelques puces.\n\n"
            f"Objet : {email['subject']}\n"
            f"Contenu : {email['body']}\n\n"
            "Fais un condensé clair, en extrayant les points clés."
        )}
    ]

    response = openai.chat.completions.create(
        model="gpt-4o-mini",  
        messages=messages,
        max_tokens=1000,
        temperature=0.7
    )

    raw_summary = response.choices[0].message.content.strip()
    formatted_summary = convert_bullets_to_html(raw_summary)  # Convertit les puces et le gras en HTML
    return formatted_summary

def send_summary_via_gmail(service, to_email, subject, summary):
    from email.mime.text import MIMEText
    import base64

    # Crée le message MIME
    message = MIMEText(summary, "html", "utf-8")
    message["to"] = to_email
    message["subject"] = subject

    # Encode le message pour l'envoyer via l'API Gmail
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    body = {"raw": raw_message}

    # Envoie le message
    sent_message = service.users().messages().send(userId="me", body=body).execute()
    return sent_message

if __name__ == "__main__":
    # Authentification Gmail
    service = gmail_authenticate()

    # Récupère les e-mails depuis un label spécifique
    emails = get_emails_from_label(service, label_name="À LIRE", max_results=20)

    if not emails:
        print("Aucun email trouvé dans le label 'À LIRE'.")
    else:
        # Génère les résumés des e-mails
        summaries = []
        for email in emails:
            summary = summarize_email_with_chat(email)
            summaries.append((email['subject'], summary))

        # Formatte le résumé en HTML
        summary_html = format_summary_as_html(summaries)

        # Envoie le résumé par e-mail
        send_summary_via_gmail(
            service=service,
            to_email="seb.albou@datafed.fr",
            subject="Résumé hebdomadaire des newsletters",
            summary=summary_html
        )

        print("Résumé envoyé avec succès !")

