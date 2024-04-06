import random
from django.core.mail import send_mail
from django.conf import settings

def login_d(request,email):
    subject=""
    em = request.session.get('email')
    message = f'{em},'
    email_from = settings.EMAIL_HOST
    send_mail(subject,message,email_from,[email])

def send_otp(request,email):
    subject = "Your OTP for Registration"
    otp = random.randint(1000,9999)
    print(otp)
    message = f"Your Otp is :{otp}"
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    request.session['otp']=otp
    return True
