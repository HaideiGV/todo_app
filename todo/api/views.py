from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import viewsets

from todo.api.models import Board, TodoItem
from todo.api.serializers import (
    UserSerializer,
    BoardListSerializer,
    TodosSerializer,
    BoardDetailSerializer,
    BoardSerializer,
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


