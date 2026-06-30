from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import Task
from tasks_app.models import Comment


class MemberSerializer(serializers.ModelSerializer):
    """Serialize a user as a board or task member."""

    fullname = serializers.CharField(
        source="userprofile.fullname", read_only=True)

    class Meta:
        model = User
        fields = ["id", "fullname", "email"]
        read_only_fields = ["email", "id", "fullname"]


class TaskSerializerCommentsCount(serializers.ModelSerializer):
    """Serialize a task including its comment count."""

    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source="assignee",
        required=False)
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source="reviewer",
        required=False)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "assignee_id",
            "reviewer",
            "reviewer_id",
            "due_date",
            "comments_count"]

    def get_comments_count(self, obj):
        """Return the number of comments on the task."""
        return obj.comments.count()


class TaskSerializer(serializers.ModelSerializer):
    """Serialize a task with nested assignee and reviewer."""

    assignee = MemberSerializer(read_only=True)
    reviewer = MemberSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source="assignee",
        required=False)
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source="reviewer",
        required=False)

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "assignee_id",
            "reviewer",
            "reviewer_id",
            "due_date"]
        read_only_fields = ["id"]


class CommentSerializer(serializers.ModelSerializer):
    """Serialize a comment with its author's full name."""

    author = serializers.SerializerMethodField()

    # The obj is the Meta class model
    def get_author(self, obj: Comment):
        """Return the full name of the comment's author."""
        return obj.author.userprofile.fullname

    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]
        read_only_fields = ["id", "created_at", "author"]
