from django.contrib.auth.models import User
from django.db import models


class Board(models.Model):
    """A Kanban board owned by one user and shared with its members."""

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_boards")
    title = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="member_boards")
