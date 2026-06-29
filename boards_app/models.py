from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_boards")
    title = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="member_boards")
