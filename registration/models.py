''' Standard '''
import datetime
from random import random

''' Django! '''
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.hashcompat import sha_constructor
from django.core.urlresolvers import (
    reverse,
    NoReverseMatch,
)

''' Contrib! '''
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
'''
TODO: We need to delete expired confirmations.  We also need to go
and make sure that we can actually send a confirmation email out there.

How will we handle multiple invites to the same user (likely just
ignore them when the user enters the webpage).
'''

class EmailConfirmationManager(models.Manager):
    def confirm_email(self, confirmation_key):
        try:
            confirmation = self.get(confirmation_key=confirmation_key)
        except self.model.DoesNotExist:
            return None

        if not confirmation.is_key_expired():
            user = confirmation.user
            user.is_active = True
            user.save()
            return user

    def send_confirmation(self, user, sent_by=None):
        salty_mail = sha_constructor(str(random())).hexdigest()[:5]
        salty_mail = salty_mail + user.email
        confirmation_key = sha_constructor(salty_mail).hexdigest()
        current_site = Site.objects.get_current()
        try:
            path = reverse("registration.views.confirm_email", \
                           args=[confirmation_key])
        except NoReverseMatch:
            path = reverse("registration_confirm_email", \
                           args=[confirmation_key])
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")

        # This will be the url from which we activte the account!
        activation_url = u"{0}://{1}{2}".format(
            protocol,
            unicode(current_site.domain),
            path,
        )
        print activation_url
        context = {
            "user": user,
            "activation_url": activation_url,
            "current_site": current_site,
            "confirmation_key": confirmation_key,
        }

        # If the email is an invite, then it will have been sent by
        # another user.  The templates are different, so make sure to
        # use the right one!
        if sent_by is not None: 
            context['sent_by'] = sent_by 
            subject_path = "registration/email_invite_subject.txt"
            message_path = "registration/email_invite_message.txt"
        else:
            subject_path = "registration/email_confirmation_subject.txt"
            message_path = "registration/email_confirmation_message.txt"
        subject = render_to_string(subject_path, context)
        message = render_to_string(message_path, context)
        
        # Join the subject into one long line.
        subject = "".join(subject.splitlines())
        send_mail(subject, message, settings.FROM_EMAIL, [user.email])

        # Determine whether to create an invite or a confirmations (again).
        # However, this time we're creating the actual server object.
        if sent_by is not None:
            confirmation = EmailInvite(
                user=user,
                sent_by=sent_by,
                sent=datetime.datetime.now(),
                confirmation_key=confirmation_key
            )
        else:
            confirmation = EmailConfirmation(
                user=user,
                sent=datetime.datetime.now(),
                confirmation_key=confirmation_key
            )
        confirmation.save()
        return confirmation

    def delete_expired(self):
        for confirmation in self.all():
            if confirmation.is_key_expired():
                confirmation.delete()

class AbstractEmailConfirmation(models.Model):
    '''
    This represents an abstract email confirmation.
    At least, the email confirmation contains a key, and is sent
    to a user for activation (the user will currently not be active
    at the time this is sent).
    '''
    user = models.ForeignKey(User)
    sent = models.DateTimeField(auto_now_add=True)
    objects = EmailConfirmationManager()
    confirmation_key = models.CharField(max_length=40)

    objects = EmailConfirmationManager()
    class Meta:
        abstract = True

    def is_key_expired(self):
            expiration_date = self.sent + datetime.timedelta(
                    days=settings.EMAIL_CONFIRMATION_DAYS)

    def __unicode__(self):
        return u"{0} Confirmation".format(self.user.email)

class EmailConfirmation(AbstractEmailConfirmation):
    '''
    This is the default type of email invite, that being the automated
    one sent from the website to a user.
    '''
    pass

class EmailInvite(AbstractEmailConfirmation):
    '''
    This is an email invite, which can be sent from one user to another.
    '''
    sent_by = models.ForeignKey(User, related_name='sent_invite_set')

    def __unicode__(self):
        return u"{0} Confirmation from {1}".format(self.user.email, \
                                                   self.sent_by.email)
