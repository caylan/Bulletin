from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseServerError,
)
from django.shortcuts import render
from models import PostNotification, CommentNotification
from gevent.event import AsyncResult
import time

class InboxNotifications(object):
    '''
    Keeps track of notifications for each user in a dictionary of user ids to
    events.

    Note: This could likely be abstracted further.
    '''
    def __init__(self):
        self.notifications = dict([])

    def _set_event(self, uid):
        if uid not in self.notifications:
            self.notifications[uid] = AsyncResult()

    def set(self, notification):
        '''
        Sets the event for the notification.
        '''
        uid = notification.user.id
        if user in self.notifications:
            self.notifications[uid].set(notification)
            del self.notifications[uid]

    def get(self, uid):
        '''
        Attempts to get all of the recently added elements in the queue.  Blocks
        until there is at least one element in the queue.  After that everything
        is pulled out and returned as an array of events.
        '''
        self._set_event(uid)
        return self.notifications[uid].get(timeout=20)

#  The set of events as mapped to each user.
notifications = InboxNotifications()

@login_required
def update(request):
    uid = request.user.id
    update_content = notifications.get(uid)
    if update_content is False:
        return HttpResponseBadRequest()
    context = {'notification': update_content}

    '''
    Make the grand assumption that this will always be a proper 
    notification.
    '''
    return render(request, 'inbox_notification.html', context)
