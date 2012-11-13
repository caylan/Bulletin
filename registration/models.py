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

We also need to change the base email manager class to be an abstract
model so that handling invites vs confirmations is a ton easier.
'''

class EmailConfirmationManager(models.Manager):
    def confirm_email(self, confirmation_key):
        try:
            confirmation = self.get(confirmation_key=confirmation_key)
        except self.model.DoesNotExist:
            return None

        if not confirmation.expired():
            user = confirmation.user
            user.is_active = True
            user.save()
            return user

    def send_confirmation(self, user):
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

        context = {
            "email": user.email,
            "activation_url": activation_url,
            "current_site": current_site,
            "confirmation_key": confirmation_key,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

        # If the email is an invite, then it will have been sent by
        # another user.  The templates are different, so make sure to
        # use the right one!
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name
        subject_path = "registration/email_confirmation_subject.txt"
        message_path = "registration/email_confirmation_message.txt"
        subject = render_to_string(subject_path, context)
        message = render_to_string(message_path, context)
        
        # Join the subject into one long line.
        subject = "".join(subject.splitlines())
        send_mail(subject, message, settings.FROM_EMAIL, [user.email])

        # Determine whether to create an invite or a confirmations (again).
        # However, this time we're creating the actual server object.
        confirmation = EmailInvite(
            user=user,
            sent_by=sent_by,
            sent=datetime.datetime.now(),
            confirmation_key=confirmation_key
        )
        confirmation.save()
        return confirmation

    def delete_expired(self):
        for confirmation in self.all():
            if confirmation.expired():
                confirmation.delete()


class AbstractConfirmation(models.Model):
    '''
    This represents an abstract confirmation.  A confirmation has an expiration
    date, and a user who must confirm said confirmation before it expires.
    '''
    user = models.ForeignKey(User)
    sent = models.DateTimeField(auto_now_add=True)

    def expired(self):
        expiration_date = self.sent + datetime.timedelta(
                days=settings.CONFIRMATION_DAYS)
        return expiration <= datetime.datetime.now()
    expired.boolean = True

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"{0} Confirmation".format(self.user)

class AbstractKeyConfirmation(AbstractConfirmation):
    '''
    An extension of the abstract confirmation, this confirmation contains a key.
    The key is intended to be used for verification.
    '''
    confirmation_key = models.CharField(max_length=4)

    class Meta:
        abstract = True

class EmailConfirmation(AbstractKeyConfirmation):
    objects = EmailConfirmationManager()
