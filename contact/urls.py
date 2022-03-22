from django.urls import path
from .views import ContactView, contact_list, generate_contacts


urlpatterns = [
    path("", ContactView.as_view(), name="contact"),
    path('list/', contact_list, name='contact_list'),
    path('generate/', generate_contacts, name='generate')
]

