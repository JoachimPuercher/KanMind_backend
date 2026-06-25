from django.urls import path
from .views import PostTaskView, TaskListSelfAssignedView, DeleteCommentView, TaskCommentView, UpdateDeleteTaskView, TasksReviewingList


urlpatterns = [
    path('tasks/assigned-to-me/', TaskListSelfAssignedView.as_view()),
    path('tasks/', PostTaskView.as_view()),
    path('tasks/reviewing/', TasksReviewingList.as_view()),
    path('tasks/<int:task_id>/', UpdateDeleteTaskView.as_view()),
    path('tasks/<int:task_id>/comments/', TaskCommentView.as_view()),
    path('tasks/<int:task_id>/comments/<int:comment_id>/', DeleteCommentView.as_view())
]
