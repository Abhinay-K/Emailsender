from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings
import json

# Create your views here.
def send_email_api(request,**kwargs):	
    if request.method == 'POST':
        body=json.loads(request.body)

        send_email_from_app(body['username'],body['mail'])
        data = {
            
            'success': True,
            'message': 'email was sent to you'
        }
    else:
        data = {
            
            'success': False,
            'message': 'Wrong email address'
        }


    return JsonResponse(data)

def send_email_from_app(username,mail):
    html_tpl_path = 'emailsender/welcome.html'
    context_data =  {'name': username}
    email_html_template = get_template(html_tpl_path).render(context_data)
    receiver_email = mail
    email_msg = EmailMessage('Welcome from django app', 
                                email_html_template, 
                                settings. APPLICATION_EMAIL,
                                [receiver_email],
                                reply_to=[settings.APPLICATION_EMAIL]
                                )
    # this is the crucial part that sends email as html content but not as a plain text
    email_msg.content_subtype = 'html'
    email_msg.send(fail_silently=False)