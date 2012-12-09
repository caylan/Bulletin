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
from gevent.queue import Empty
from gevent.queue import Queue
from gevent.coros import Semaphore
import time

class InboxNotifications(object):
    '''
    Keeps track of notifications for each user in a dictionary of user ids to
    events.

    Note: This could likely be abstracted further.
    '''
    def __init__(self):
        self.notifications = dict([])
        self.locks = dict([])

    def _set_queue(self, uid):
        if uid not in self.notifications:
            self.notifications[uid] = Queue()
            self.locks[uid] = Semaphore()

    def put(self, notification):
        '''
        Sets the event for the notification.
        '''
        user_id = notification.user.pk
        self._set_queue(user_id)
        self.notifications[user_id].put(notification)

    def lock(self, uid):
        '''
        Returns a lock to the queue corresponding to the uid.  If one would like
        to prevent deadlock whilst reading from the queue, make sure to disable
        blocking while reading from the queue.

        In order to use the lock, one must create either a) a sandwich of lock
        acquisition and release, or b) a with statement using the lock.

        ex:

        obj.lock(123).acquire()
        do_work()
        obj.lock(123).release()

        #  ^ this is ugly, though, so the following is preferred.

        with obj.lock(123):
            do_work()
        # now the lock has been released!
        '''
        self._set_queue(uid)
        return self.locks[uid]

    def get(self, user_id, blocking=True):
        '''
        Attempts to get all of the recently added elements in the queue.  Blocks
        until there is at least one element in the queue.  After that everything
        is pulled out and returned as an array of events.
        '''
        res = []
        self._set_queue(user_id)
        while True:
            try:
                if blocking:
                    res.append(self.notifications[user_id].get())
                else:
                    res.append(self.notifications[user_id].get_nowait())
            except Empty:
                break
            if self.notifications[user_id].qsize() == 0:
                break
        return res

#  The set of events as mapped to each user.
notifications = InboxNotifications()

@login_required
def update(request):
    # NOTE:  Using a lock here will cause deadlock.  Better to have odd issues
    # than deadlock (this happens because a lock must be acquired to put an
    # update when running a post, but this could potentially block).
    update_content = notifications.get(request.user.pk)
    context = {'notifications': update_content}

    '''
    Make the grand assumption that this will always be a proper list of
    notification classes.

    TODO: Perhaps enforce this some way...
    '''
    return render(request, 'inbox_notification_list.html', context)
