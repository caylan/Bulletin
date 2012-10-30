''' Standard '''
import datetime
from random import random

''' Django! '''
from django.db import models
from django.utils.hashcompat import sha_constructor

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

        if not confirmation.key_expired():
            user = confirmation.user
            user.is_active = True
            user.save()
            return user

    def send_confirmation(self, user, sent_by=None):
        salty_mail = sha_constructor(str(random())).hexdigest()[:5]
        salty_mail = salty_mail + user.email
        confirmation_key = sha_constructor(salty_mail).hexdigest()
        ''' TODO: We have a confirmation key!  Now send it off... '''


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
