from __future__ import absolute_import, unicode_literals

import logging
from django.core import mail

from todo.api.models import Reminder
from todo.celery import app


log = logging.getLogger(__name__)


@app.task
def send_reminder(reminder_id, **kwargs):
    try:
        reminder = Reminder.objects.get(pk=reminder_id)
    except Reminder.DoesNotExist:
        log.error(f"Reminder[{reminder_id}] not found or already deleted.")
        return

    with mail.get_connection() as connection:
        mail.EmailMessage(
            '[Reminder]',
            reminder.text,
            'noreply@example.com',
            [reminder.email],
            connection=connection
        ).send()