''' Standard '''
import datetime
from random import random

''' Django! '''
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.hashcompat import sha_constructor
from djangot.core.exceptions import DoesNotExist
from django.core.urlresolvers import (
    reverse,
    NoReverseMatch,
)

''' Contrib! '''
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

''' Bulletin Models! '''
from groups.models import Group

'''
TODO: We need to delete expired confirmations.
'''

class EmailConfirmationManager(models.Manager):
    '''
    Manages sending confirmation emails to users that are to be (eventually)
    registered on the website.
    '''

    # If extra fields for when the message is to be sent, this is appended.  An
    # alternative should be sought however, as this isn't best practice.
    email_context = {}
    subject_path = "registration/email_confirmation_subject.txt"
    message_path = "registration/email_confirmation_message.txt"
    view_path = "registration.views.confirm_email"

    def confirm_email(self, confirmation_key):
        try:
            confirmation = self.get(confirmation_key=confirmation_key)
        except self.model.DoesNotExist:
            return None

        if not confirmation.expired():
            user = confirmation.user
            user.is_active = True
            user.save()
            confirmation.delete() # remove old invite.
            return user

    def send_confirmation(self, user, commit=True):
        salty_mail = sha_constructor(str(random())).hexdigest()[:5]
        salty_mail = salty_mail + user.email
        confirmation_key = sha_constructor(salty_mail).hexdigest()
        current_site = Site.objects.get_current()
        path = reverse(self.view_path, args=[confirmation_key])
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")

        # This will be the url from which we activte the account!
        activation_url = u"{0}://{1}{2}".format(
            protocol,
            unicode(current_site.domain),
            path,
        )

        self.email_context.update({
            "email": user.email,
            "activation_url": activation_url,
            "current_site": current_site,
            "confirmation_key": confirmation_key,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })

        # If the email is an invite, then it will have been sent by
        # another user.  The templates are different, so make sure to
        # use the right one!
        self.email_context['first_name'] = user.first_name
        self.email_context['last_name'] = user.last_name
        subject = render_to_string(self.subject_path, self.email_context)
        message = render_to_string(self.message_path, self.email_context)
        
        # Join the subject into one long line.
        subject = "".join(subject.splitlines())
        send_mail(subject, message, settings.FROM_EMAIL, [user.email])

        # Determine whether to create an invite or a confirmations (again).
        # However, this time we're creating the actual server object.
        confirmation = self.model(
            user=user,
            sent=datetime.datetime.now(),
            confirmation_key=confirmation_key
        )
        if commit:
            confirmation.save()
        return confirmation

    def delete_expired(self):
        for confirmation in self.all():
            if confirmation.expired():
                confirmation.delete()

class EmailInviteManager(EmailConfirmationManager):
    subject_path = "registration/email_invite_subject.txt"
    message_path = "registration/email_invite_message.txt"
    view_path = "registration.views.confirm_email_invite"

    def send_confirmation(self, sender, recipient, group):
        self.email_context['sender_email'] = sender.email
        self.email_context['recipient_is_active'] = recipient.is_active
        self.email_context['group'] = group.name 
        confirmation = super(EmailInviteManager, self).send_confirmation(
                recipient, commit=False)
        confirmation.group = group
        confirmation.save()

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
        return expiration_date <= timezone.now()
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

class EmailInvite(AbstractKeyConfirmation):
    objects = EmailInviteManager()
    group = models.ForeignKey(Group)

    def save(self, *args, **kwargs):
        '''
        Override of original save function.  This ensures that the user is not
        already in the group the invite is for.  It would be silly to send an
        invite to the user for a group they are already in.
        '''
        try:
            self.group.members.all().get(id=self.user.id)
            raise Exception, "invite cannot be to a user already in this group" 
        except DoesNotExist:
            super(EmailInvite, self).save()
