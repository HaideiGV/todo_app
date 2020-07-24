from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from todo.api.tasks import send_reminder

from todo.api.models import Board, TodoItem, Reminder
from todo.api.serializers import (
    UserSerializer,
    BoardListSerializer,
    TodosSerializer,
    BoardDetailSerializer,
    BoardSerializer,
    ReminderSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.annotate(todo_count=Count('todos')).all()
    serializer_class = BoardDetailSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return BoardListSerializer
        elif self.action == 'retrieve':
            return BoardDetailSerializer
        else:
            return BoardSerializer



class TodoItemViewSet(viewsets.ModelViewSet):
    queryset = TodoItem.objects.all()
    serializer_class = TodosSerializer



class ReminderViewSet(
    CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(True)
        serializer.save()
        send_reminder.apply_async(
            args=[serializer.instance.id], countdown=serializer.instance.delay
        )
        return Response(data=serializer.data, status=HTTP_200_OK)
