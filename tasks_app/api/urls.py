from django.urls import path
from .views import PostTaskView, TaskListSelfAssignedView

urlpatterns = [
    path('tasks/assigned-to-me/', TaskListSelfAssignedView.as_view()),
    path('tasks/', PostTaskView.as_view()),
]
