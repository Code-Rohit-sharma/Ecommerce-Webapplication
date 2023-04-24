from django.core.mail import EmailMessage

from celery import shared_task

@shared_task
def send_mail_password_reset(receiver_email,reset_url):
    #sender mail

    subject="Reset Password"
    message = reset_url
    reply_to_list=[receiver_email]    
    email = EmailMessage(subject,message,'girishshrma750@gmail.com',reply_to_list)
    email.send(fail_silently=True)
    return "Task Completed"

@shared_task
def send_mail_activation_link(receiver_email,activation_link):

    #send mail
    subject="Activation Link"
    message = activation_link
    reply_to_list=[receiver_email]    
    email = EmailMessage(subject,message,'girishshrma750@gmail.com',reply_to_list)
    email.send(fail_silently=True)

    return "Task Completed"