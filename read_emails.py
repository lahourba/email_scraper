import base64

def get_emails_from_label(service, label_name='À LIRE', max_results=20):
    # Recherchez le label ID correspondant au label_name
    response = service.users().labels().list(userId='me').execute()
    labels = response.get('labels', [])
    
    label_id = None
    for label in labels:
        if label['name'] == label_name:
            label_id = label['id']
            break
    
    if not label_id:
        print(f"Le label {label_name} n'existe pas.")
        return []
    
    # Requête pour lister les messages associés au label
    messages_list = service.users().messages().list(
        userId='me',
        labelIds=[label_id],
        maxResults=max_results,
        q="newer_than:7d"
    ).execute()
    
    messages = messages_list.get('messages', [])
    result = []
    
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        
        # Récupération du corps du mail (version texte ou html)
        payload = msg_data.get('payload', {})
        
        # On peut récupérer toutes les parties du payload
        parts = payload.get('parts', [])
        email_text = ""
        
        # Parfois le texte se trouve directement dans "payload['body']"
        if 'body' in payload and 'data' in payload['body']:
            email_text += base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
        
        # Parcours des différentes parties pour trouver le text/plain ou text/html
        for part in parts:
            mime_type = part.get('mimeType')
            body = part.get('body', {})
            data = body.get('data')
            if data:
                text_part = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                email_text += f"\n{text_part}"
        
        # Récupération de l’objet
        headers = msg_data.get('payload', {}).get('headers', [])
        subject = ""
        for header in headers:
            if header['name'].lower() == 'subject':
                subject = header['value']
                break
        
        result.append({
            'id': msg['id'],
            'subject': subject,
            'body': email_text
        })
    
    return result
