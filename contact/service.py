from django.core.mail import send_mail


def send(user_email):
    send_mail(
        'Вы подписались на рассылку сайта все о кино',
        "Мы будем присылать вам все новости",
        'vitaliikondratiev@ukr.net',
        [user_email],
        fail_silently=False,
    )