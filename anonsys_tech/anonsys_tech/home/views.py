from django.http import HttpRequest, HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
# from django.core.mail import EmailMessage
# from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ContactForm
from .decorators import check_recaptcha


# Create your views here.


def index(request):
    if request.method == 'POST':
    search_ip = request.POST.get('search_ip', None)
    try:
        return HttpResponseRedirect("/ip/%s" % search_ip)
    except:
        print("something went wrong...")
        return HttpResponseBadRequest

    
    assert isinstance(request, HttpRequest)
    context = {
        'title' : 'Home Page',
        'search_type' : 'popcorntime',
    }
    return render(request, 'index.html', context)

@check_recaptcha
def contact(request):
     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid() and request.recaptcha_is_valid:
            # process the data in form.cleaned_data as required
            subject = "Contact Form - "+form.cleaned_data['subject']
            body = form.cleaned_data['message']
            contacter = form.cleaned_data['sender']
            # cc_myself = form.cleaned_data['cc_myself']
            to_list = ['support@anonsys.tech']
            bcc_list = []
            cc_list = []
            replyto_list = []
            # if cc_myself:
            #     bcc_list.append(contacter)
            text_content = f'''Contact Form: \n
                                From: {contacter}
                                Subject: {subject}
                                Message:
                                {body}'''
            html_content = f"<h3>Contact Form:</h3><h5>From: {contacter}</h5><h5>Subject: </h5>{subject}<h5>Message: </h5>{body}"
            msg = EmailMultiAlternatives(subject=subject, body=html_content, from_email=contacter, to=to_list,
                                         bcc=bcc_list, connection=None, attachments=None, headers=None,
                                         alternatives=None, cc=cc_list, reply_to=replyto_list)
            msg.attach_alternative(text_content, "text/html")

            # send_mail(subject, message, sender, recipients)
            msg.send()
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
    if request.method == 'POST':
    search_ip = request.POST.get('search_ip', None)
    try:
        return HttpResponseRedirect("/ip/%s" % search_ip)
    except:
        print("something went wrong...")
        return HttpResponseBadRequest
    
    assert isinstance(request, HttpRequest)
    context = {
        'title': 'Thanks for your feedback!',
        'search_type': 'search_ip',
    }
    return render(request, 'thx.html', context)
