from django.urls import path
from .views import AllBoardsView

urlpatterns = [
    path('boards/', AllBoardsView.as_view())
]
