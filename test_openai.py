import openai
import os

# Option : si tu utilises python-dotenv, tu peux le charger ici
# from dotenv import load_dotenv
# load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")  # Récupère la clé depuis la variable d'env

def summarize_emails_with_chat(emails):
    all_text = ""
    for email in emails:
        all_text += f"Objet: {email['subject']}\nContenu: {email['body']}\n\n"

    messages = [
        {"role": "system", "content": "Tu es un assistant chargé de résumer des newsletters."},
        {"role": "user", "content": (
            "Voici plusieurs newsletters à résumer en français, en quelques puces. "
            "Fais un condensé clair, en extrayant les points clés.\n\n"
            f"{all_text}"
        )}
    ]

    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # ou "gpt-3.5-turbo"
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )
    
    summary = response.choices[0].message.content.strip()
    return summary


if __name__ == "__main__":
    # Petit test local
    # On simule une liste d'e-mails
    fake_emails = [
        {
            'subject': 'Newsletter sur la Data',
            'body': "Bonjour, ceci est un test. On parle ici de data, d'IA, etc."
        },
        {
            'subject': 'Actu IA 2024',
            'body': "Voici quelques nouveautés en Intelligence Artificielle..."
        }
    ]

    # On appelle la fonction de résumé
    test_summary = summarize_emails_with_chat(fake_emails)

    # On affiche le résultat
    print("=== RÉSUMÉ DE TEST ===")
    print(test_summary)
