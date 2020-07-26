from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from todo.api.views import BoardViewSet, TodoItemViewSet, ReminderViewSet, signup_view

router = routers.DefaultRouter()
router.register(r'api/boards', BoardViewSet)
router.register(r'api/todos', TodoItemViewSet)
router.register(r'api/reminders', ReminderViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/signup/', signup_view),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
