from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from django.shortcuts import redirect, render
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions

from todo.api.permissions import IsOwner, IsBoardOwner
from todo.api.tasks import send_reminder

from todo.api.models import Board, TodoItem, Reminder
from todo.api.serializers import (
    BoardListSerializer,
    TodosSerializer,
    BoardDetailSerializer,
    BoardSerializer,
    ReminderSerializer,
)


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.annotate(todo_count=Count('todos')).all()
    serializer_class = BoardDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        if self.action == 'list':
            return (
                Board
                .objects
                .filter(user=user)
                .annotate(todo_count=Count('todos'))
                .all()
            )
        else:
            return Board.objects.filter(user=user).all()

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
    permission_classes = [permissions.IsAuthenticated, IsBoardOwner]

    def get_queryset(self):
        user = self.request.user
        return TodoItem.objects.filter(board__user=user).all()


class ReminderViewSet(
    CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


    def get_queryset(self):
        user = self.request.user
        return Reminder.objects.filter(user=user).all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(True)
        serializer.save()
        send_reminder.apply_async(
            args=[serializer.instance.id], countdown=serializer.instance.delay
        )
        return Response(data=serializer.data, status=HTTP_200_OK)


def signup_view(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    return render(request, 'registration/sign_up.html', {'form': form})
