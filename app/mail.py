import requests
from app import app

def send_email(sender, recipient, subject, body):
    url = "https://api.postman.com/email"

    headers = {
        "X-Api-Key": app.config['POSTMAN_MAILER_API_KEY'],
        "Content-Type": "application/json"
    }

    payload = {
        "from": sender,
        "to": recipient,
        "subject": subject,
        "text": body
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Email sent successfully")
    else:
        print("Failed to send email")
        print(response.text)
