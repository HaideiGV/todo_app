from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from django.db.models import CASCADE


class Board(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)


class TodoItem(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    done = models.BooleanField(default=False, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    board = models.ForeignKey(Board, on_delete=CASCADE, related_name='todos')


class Reminder(models.Model):
    email = models.EmailField(blank=False, null=False)
    text = models.CharField(max_length=512, null=False, blank=False)
    delay = models.PositiveIntegerField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="reminders")

