from django.db import models
from django.contrib.auth.models import User
from django. utils import timezone


class Board(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_boards")
    title = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="member_boards")


    # All counts calculated in serialzer:
    # member_count = models.IntegerField()
    # ticket_count = models.IntegerField()
    # tasks_to_do_count = models.IntegerField()
    # tasks_high_prio_count = models.IntegerField()