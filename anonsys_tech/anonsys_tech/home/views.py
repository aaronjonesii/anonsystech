from django.http import HttpRequest, HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ContactForm

# Create your views here.


def index(request):

    assert isinstance(request, HttpRequest)
    context = {
        'title' : 'Home Page',
        'search_type' : 'popcorntime',
    }
    return render(request, 'index.html', context)


def contact(request):
     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            if form.is_valid():
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                sender = form.cleaned_data['sender']
                cc_myself = form.cleaned_data['cc_myself']

                recipients = ['support@anonsys.tech']
                if cc_myself:
                    recipients.append(sender)

                send_mail(subject, message, sender, recipients)
                return HttpResponseRedirect('/thx/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()

    assert isinstance(request, HttpRequest)
    context = {
        'title': 'Contact Page',
        'search_type': 'search_ip',
        'form': form,
    }
    return render(request, 'contact.html', context)


def thx(request):
    assert isinstance(request, HttpRequest)
    context = {
        'title': 'Thanks for your feedback!',
        'search_type': 'search_ip',
    }
    return render(request, 'thx.html', context)
