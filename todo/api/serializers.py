from django.contrib.auth.models import User
from rest_framework import serializers

from todo.api.models import Board, TodoItem, Reminder


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']



class TodosSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TodoItem
        exclude = ('created_at', 'updated_at', )


class ReminderSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        user = self.context['request'].user
        return Reminder.objects.create(user=user, **validated_data)

    class Meta:
        model = Reminder
        fields = ("text", "email", "delay", "url")


class BoardSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        user = self.context['request'].user
        return Board.objects.create(user=user, **validated_data)

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