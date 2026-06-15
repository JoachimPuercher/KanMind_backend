from django.urls import path
from .views import PostTaskView, TaskListSelfAssignedView
from .views import TaskCommentView

urlpatterns = [
    path('tasks/assigned-to-me/', TaskListSelfAssignedView.as_view()),
    path('tasks/', PostTaskView.as_view()),
    path('tasks/<int:task_id>/comments/', TaskCommentView.as_view())
]
