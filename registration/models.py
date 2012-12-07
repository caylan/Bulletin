''' Standard '''
import datetime
from random import random

''' Django! '''
from django.db import models
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.hashcompat import sha_constructor
from django.core.exceptions import ObjectDoesNotExist
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
TODO: Delete confirmations if we detect that, somehow, the email was not
delivered successfully to the user.
'''

class EmailConfirmationManager(models.Manager):
    '''
    Manages sending confirmation emails to users that are to be (eventually)
    registered on the website.
    '''

    # If extra fields for when the message is to be sent, this is appended.  An
    # alternative should be sought however, as this isn't best practice.
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
            return user
    
    def create_key(self, email):
        salty_mail = sha_constructor(str(random())).hexdigest()[:5]
        salty_mail = salty_mail + email
        confirmation_key = sha_constructor(salty_mail).hexdigest()
        return confirmation_key

    def create_activation_url(self, key):
        current_site = Site.objects.get_current()
        path = reverse(self.view_path, args=[key])
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")

        # This will be the url from which we activte the account!
        activation_url = u"{0}://{1}{2}".format(
            protocol,
            unicode(current_site.domain),
            path,
        )
        return (activation_url, current_site)

    def send_mail(self, contexts, mass_mail=False):
        '''
        Sends a list of emails (using mass_mail if specified) to a list of
        contexts.
        
        Following this method:
          https://docs.djangoproject.com/en/dev/topics/email/?from=olddocs

        message1 = ('Subject here', 'Here is the message', 'from@example.com',
        ['first@example.com', 'other@example.com'])

        message2 = ('Another Subject', 'Here is another message',
                'from@example.com', ['second@test.com'])

        send_mass_mail((message1, message2), fail_silently=False)
        '''
        mail_list = []
        for ctx in contexts:
            subject = render_to_string(self.subject_path, ctx)
            # Join the subject into one long line.
            subject = "".join(subject.splitlines())
            message = render_to_string(self.message_path, ctx)
            mail_list.append(
                (subject, message, settings.FROM_EMAIL, [ctx['email']])
            )
        
        # Send out the mass mail!
        send_mass_mail(
            mail_list,
            fail_silently=False,
        )

    def send_confirmation(self, user):
        key = self.create_key(user.email)
        (activation_url, current_site) = self.create_activation_url(key)
        email_context = {
            "email": user.email,
            "activation_url": activation_url,
            "current_site": current_site,
            "confirmation_key": key,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

        # Determine whether to create an invite or a confirmations (again).
        # However, this time we're creating the actual server object.
        confirmation = self.model(
            user=user,
            confirmation_key=key,
        )
        confirmation.save()

        # If we're here and an exception hasn't been thrown, then we'll send off
        # the email.
        self.send_mail([email_context])
        return confirmation

    def delete_expired(self):
        for confirmation in self.all():
            if confirmation.expired():
                confirmation.delete()

class EmailInviteManager(EmailConfirmationManager):
    subject_path = "registration/email_invite_subject.txt"
    message_path = "registration/email_invite_message.txt"
    view_path = "registration.views.confirm_email_invite"

    def send_confirmation(self, sender, recipient_emails, group):
        '''
        Sends an email invite to recipient email.  This assumes that the
        recipient email is valid, and that the sender is a valid active user.
        '''
        # Iterate through all emails and send one big scary mass email!
        # each email will have an individual email sent to each recipient.
        email_context_lst = []
        confirmation_lst = []
        for email in recipient_emails:
            # Check to see if the recipient email is active.
            try:
                recipient = User.objects.all().get(email=email)
            except User.DoesNotExist:
                recipient = False

            #  Create email context for subject and messages.  Creates key, gets
            #  active site, and the active URL.
            key = self.create_key(email)
            (activation_url, current_site) = self.create_activation_url(key)
            email_context = {
                'recipient_is_active': bool(recipient),
                'sender_email': sender,
                'group': group.name,
                "email": email,
                "activation_url": activation_url,
                "current_site": current_site,
                "confirmation_key": key,
            }

            # If the recipient is an active user, put their first/last name in the
            # email context.
            if recipient:
                email_context['first_name'] = recipient.first_name
                email_context['last_name'] = recipient.last_name

            #  Create the confirmation from the data we've accrued.  Any exceptions
            #  will be thrown here and put upstream (this has to happen before
            #  attempting to send the email).
            confirmation = self.model(
                group=group,
                recipient_email=email,
                confirmation_key=key,
            )
            confirmation.group = group

            # The commit is off so we can throw any exceptions due to invalid
            # emails (ones where the user is already a part of this group, for
            # example).
            try:
                # For now,simply ignore this one silently.
                confirmation.save(commit=False)
            except EmailInvite.MemberExists:
                continue

            confirmation_lst.append(confirmation)
            email_context_lst.append(email_context)

        # Send off the email and return the invite.
        for conf in confirmation_lst:
            conf.save()
        super(EmailInviteManager, self).send_mail(email_context_lst)
        return confirmation_lst

    def confirm_email(self, confirmation_key):
        '''
        This does not set the user to active or really 'confirm' the email.

        TODO: Reimplement this as another function.
        '''
        try:
            confirmation = self.get(confirmation_key=confirmation_key)
        except self.model.DoesNotExist:
            return None

        if not confirmation.expired():
            try:
                user = User.objects.get(email=confirmation.recipient_email)
            except User.DoesNotExist:
                user = None
            return user

    def get_email(self, key):
        try:
            confirmation = self.get(confirmation_key=key)
        except self.model.DoesNotExist:
            return None

        if not confirmation.expired():
            return confirmation.recipient_email
        return None

class AbstractConfirmation(models.Model):
    '''
    This represents an abstract confirmation.  A confirmation has an expiration
    date, and a user who must confirm said confirmation before it expires.
    '''
    sent = models.DateTimeField(auto_now_add=True)

    def expired(self):
        expiration_date = self.sent + datetime.timedelta(
                days=settings.CONFIRMATION_DAYS)
        return expiration_date <= timezone.now()
    expired.boolean = True

    class Meta:
        abstract = True

class AbstractKeyConfirmation(AbstractConfirmation):
    '''
    An extension of the abstract confirmation, this confirmation contains a key.
    The key is intended to be used for verification.
    '''
    confirmation_key = models.CharField(max_length=40)

    class Meta:
        abstract = True

class EmailConfirmation(AbstractKeyConfirmation):
    '''
    This extends the abstract key confirmation, and is tied to a user and an
    email.
    '''
    user = models.ForeignKey(User)
    objects = EmailConfirmationManager()

class EmailInvite(AbstractKeyConfirmation):
    '''
    An email invite is sent to a recipient email, which will later be checked in
    the database as to whether there is a user with this email already.

    This is because if a user is given an email confirmation and they choose to
    blow it off (and they're not already a member of the website), then they can
    still register independent of the invite given to them, which would not be
    possible by creating an inactive user.
    '''
    objects = EmailInviteManager()
    group = models.ForeignKey(Group)
    recipient_email = models.EmailField()

    # mark EmailInvite object as either pending, accepted, or rejected.
    #   pending - person who this invite was sent to has not yet acted on this
    #             invite
    #   accept  - person accepted the invite and should now be a member of the
    #             group the invite represents
    #   reject  - person rejected the invite and probably doesn't want to be
    #             part of the group
    acceptance = models.CharField(max_length=1,
                                  choices=(
                                      ('P', 'pending'),
                                      ('A', 'accept'),
                                      ('R', 'reject'),
                                  ),
                                  default='P')  # default='pending'

    class MemberExists(Exception):
        '''
        An exception within EmailInvite that is raised when a member with the
        given email already exists in the target group, thus preventing a save
        from occurring.
        '''
        pass

    def save(self, *args, **kwargs):
        '''
        Override of original save function.  This ensures that the user is not
        already in the group the invite is for.  It would be silly to send an
        invite to the user for a group they are already in.
        '''
        try:
            self.group.members.all().get(email=self.recipient_email)
            raise self.MemberExists("invite cannot be to a user" \
                    " already in this group")
        except ObjectDoesNotExist:
            super(EmailInvite, self).save()

    def __unicode__(self):
        return u'{0}'.format(self.recipient_email)
