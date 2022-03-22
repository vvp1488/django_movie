from django.core.mail import send_mail
from faker import Faker
from .models import Contact


def send(user_email):
    send_mail(
        'Вы подписались на рассылку сайта все о кино',
        "Мы будем присылать вам все новости",
        'vitaliikondratiev@ukr.net',
        [user_email],
        fail_silently=False,
    )


def create_fake_contact(num):
    fake = Faker()
    for x in range(0, num):
        Contact.objects.create(email=fake.email())