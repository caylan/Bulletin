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
from gevent.queue import Queue as GQueue
import time

class InboxNotifications(object):
    '''
    Keeps track of notifications for each user in a dictionary of user ids to
    events.

    Note: This could likely be abstracted further.
    '''
    def __init__(self):
        self.notifications = dict([])

    def put(self, notification):
        '''
        Sets the event for the notification.
        '''
        user_id = notification.user.pk
        if user_id not in self.notifications:
            self.notifications[user_id] = GQueue()
        self.notifications[user_id].put(notification)

    def get(self, user_id):
        '''
        Attempts to get all of the recently added elements in the queue.  Blocks
        until there is at least one element in the queue.  After that everything
        is pulled out and returned as an array of events.
        '''
        res = []
        if user_id not in self.notifications:
            self.notifications[user_id] = GQueue()
        while True:
            res.append(self.notifications[user_id].get())
            if self.notifications[user_id].qsize() == 0:
                break
        return res

#  The set of events as mapped to each user.
notifications = InboxNotifications()

@login_required
def update(request):
    update_content = notifications.get(request.user.pk)
    context = {'notifications': update_content}

    '''
    Make the grand assumption that this will always be a proper list of
    notification classes.

    TODO: Perhaps enforce this some way...
    '''
    return render(request, 'inbox_notification.html', context)
