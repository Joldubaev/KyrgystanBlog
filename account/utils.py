from django.core.mail import send_mail


def send_activation_code(eamil, activation_code):
    activation_url = f"http://localhost:8000/v1/api/account/activate/{activation_code}"
    message = f"""
        Thank you singing up 
        Please, activate your account.
        Activation link: {activation_url}
"""
    send_mail(
        'Activate your account',
        message,
        'test@test.com',
        [eamil, ],
        fail_silently=False
    )