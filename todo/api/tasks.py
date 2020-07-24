from __future__ import absolute_import, unicode_literals

import logging
from django.core.mail import send_mail

from todo.api.models import Reminder
from todo.celery import app


log = logging.getLogger(__name__)


@app.task
def send_reminder(reminder_id, **kwargs):
    try:
        reminder = Reminder.objects.get(pk=reminder_id)
    except Reminder.DoesNotExists:
        log.error(f"Reminder[{reminder_id}] not found.")
        return

    send_mail(
        subject='[Reminder]',
        message=reminder.text,
        from_email='noreply@example.com',
        recipient_list=[reminder.email],
        fail_silently=False,
    )
    print("DATA  >>> ", reminder_id, reminder.text, reminder.email, reminder.delay)
