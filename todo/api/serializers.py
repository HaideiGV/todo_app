from django.contrib.auth.models import User
from rest_framework import serializers

from todo.api.models import Board, TodoItem


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']



class TodosSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TodoItem
        exclude = ('created_at', 'updated_at', )


class BoardSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Board
        fields = ('name', "url")


class BoardListSerializer(serializers.HyperlinkedModelSerializer):
    todo_count = serializers.SerializerMethodField()

    def get_todo_count(self, obj):
        return obj.todo_count

    class Meta:
        model = Board
        fields = ('name', 'todo_count', "url")


class BoardDetailSerializer(serializers.HyperlinkedModelSerializer):
    todos = TodosSerializer(many=True)

    class Meta:
        model = Board
        fields = ('name', "url", "todos")