from django.core.mail import send_mail
import random, threading

def generate_code():
    return f'{random.randint(0, 999999):06d}'

def _send_verification_mail(email, code):
    send_mail(
        subject='Підтвердження пошти',
        message=f'Ваш код підтвердження: {code}.\nВін буде дійсний протягом 15 хвилин.',
        recipient_list=[email],
        from_email=None
    )

def send_verification_mail_async(email, code):
    try:
        threading.Thread(
            target=_send_verification_mail,
            args=(email, code)
        ).start()
    except Exception:
        print('ERROR')