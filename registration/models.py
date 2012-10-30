import datetime
from django.contrib.auth.models import User
from django.db import models
'''
TODO: We need to delete expired confirmations.  We also need to go
and make sure that we can actually send a confirmation email out there.
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
    sent_by = models.ForeignKey(User)

    def __unicode__(self):
        return u"{0} Confirmation from {1}".format(self.user.email, \
                                                   self.sent_by.email)
