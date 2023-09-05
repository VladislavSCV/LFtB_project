import os
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from email.mime.text import MIMEText

def send_email(sender_email, recipient_email, subject, body):
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    # Если у вас уже есть файл с учетными данными сервисного аккаунта Google, укажите его здесь.
    # В противном случае, просто оставьте пустым и при первом запуске приложения будет открыто окно авторизации.
    credentials_file = 'credentials.json'

    if os.path.exists('token.json'):
        creds = service_account.Credentials.from_service_account_file(credentials_file, scopes=SCOPES)
    # Если учетные данные просрочены или отсутствуют, приложение запросит у вас новый токен.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = service_account.Credentials.from_service_account_file(credentials_file, scopes=SCOPES). \
                authorize_entity()
            creds = flow.run_local_server(port=0)
        # Сохраняем токен для последующих запусков приложения
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)

        message = MIMEText(body)
        message['to'] = recipient_email
        message['from'] = sender_email
        message['subject'] = subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes())
        encoded_message = encoded_message.decode()

        service.users().messages().send(userId='me', body={'raw': encoded_message}).execute()
        print('Письмо успешно отправлено.')
    except HttpError as error:
        print(f'Ошибка: {error}')

# Пример использования
sender_email = 'your_email@gmail.com'
recipient_email = 'recipient_email@example.com'
subject = 'Привет!'
body = 'Привет от Python!'

send_email(sender_email, recipient_email, subject, body)