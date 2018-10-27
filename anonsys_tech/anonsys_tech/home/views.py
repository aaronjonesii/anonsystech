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
                subject = form.cleaned_data['subject']
                body = form.cleaned_data['message']
                contacter = form.cleaned_data['sender']
                cc_myself = form.cleaned_data['cc_myself']

                to_list = ['support@anonsys.tech']
                bcc_list = []
                # if cc_myself:
                #     bcc_list.append(contacter)

                text_content = f"From: {contacter}\n{body}"
                html_content = f"<h1>You recieved a new message from the contact form:</h1><br /><strong>From: {contacter}</strong><br /><p>{body}</p>"
                msg = EmailMultiAlternatives(subject, text_content, contacter, to_list)
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                # send_mail(subject, message, sender, recipients)
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
