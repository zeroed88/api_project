from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User as DjangoUser, UserManager as DjangoUserManager
from django.db.models.signals import post_save
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin
from rest_framework_jwt.utils import jwt_decode_handler
from utils.utils import getConfirmationLink

class UserManager(DjangoUserManager):

    def get_from_auth(self, auth):
        currentUserID = jwt_decode_handler(auth)['user_id']
        return super(UserManager, self).get_queryset().get(pk=currentUserID)

class User(SimpleEmailConfirmationUserMixin, DjangoUser):

    def send_new_confirmation_key(self, email=None, key=None):
        curEmail = self.email if email is None else email
        curKey = self.reset_email_confirmation(curEmail) if key is None else key
        send_mail(
            'New confirmation email',
            'Your new code is {}'.format(curKey),
	    settings.EMAIL_HOST_USER,
            [curEmail]
        )

    def update_password(self, password):
        self.set_password(password)
        self.save()

    objects = UserManager()


def HTMLmsg(link):
    tmpHTML = 'email/reg.html'
    msg = render_to_string(tmpHTML, {'url': link, 'help_email': settings.ADMIN_EMAIL})
    return msg


def send_confirmation_email(sender, **kwargs):
	# only for new users
    if kwargs['created']: 
        new_user = kwargs['instance']
        new_user.add_unconfirmed_email(new_user.email)
        link = getConfirmationLink(
            new_user.email, 
            new_user.confirmation_key, 
            settings.CURRENT_URL
        ) 
        html_msg = HTMLmsg(link)

        result = send_mail(
            'Регистрация на сайте {}'.format(settings.CURRENT_URL),
            'Для завершения регистрации кликните по ссылке: {}'.format(link),
            settings.EMAIL_HOST_USER,
            [new_user.email],
            html_message=html_msg
        )


post_save.connect(send_confirmation_email, sender=User)
