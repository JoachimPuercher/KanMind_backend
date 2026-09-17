from django.contrib.auth.models import User
from django.db import models
from boards_app.models import Board

# Create your models here.


class Priority(models.TextChoices):
    """Priority levels a task can have."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(models.TextChoices):
    """Columns a task can sit in on the board."""

    TO_DO = "to-do"
    IN_PROGRESS = "in-progress"
    REVIEW = "review"
    DONE = "done"


class Task(models.Model):
    """A card on a board, with an assignee and a reviewer."""

    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name="tasks")
    title = models.CharField(max_length=80)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices)
    priority = models.CharField(max_length=20, choices=Priority.choices)
    assignee = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="assignee_tasks")
    reviewer = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="reviewer_tasks")
    due_date = models.DateField()
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="owned_tasks")


class Comment(models.Model):
    """A comment written by a board member on a task."""

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        max_length=30,
        related_name="users")
    content = models.CharField(max_length=200)
