from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView

from django.db.models import Sum, Count

from .models import Contact
from .forms import ContactForm
from .tasks import send_spam_email, new_fake_contact


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.save()
        send_spam_email.delay(form.instance.email)
        return super().form_valid(form)


def contact_list(request):
    c_count = Contact.objects.all().count()
    return render(request, 'contact/data.html', context={'c_count': c_count })


def generate_contacts(request):
    new_fake_contact.delay(int(request.POST['count'])+1)
    return HttpResponseRedirect(reverse('contact_list'))

