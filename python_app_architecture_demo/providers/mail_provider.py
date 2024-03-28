class MailProvider:

    def __init__(self, api_token: str):
        self._api_token = api_token # You probably need private credentials to send mail

    def send_mail(self, email: str, message: str):
        print(f"Sending mail to {email}: {message}") # Simulate sending mail
