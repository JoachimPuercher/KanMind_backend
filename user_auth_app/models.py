from django.db import models
from django.contrib.auth.models import User
from django. utils import timezone
# Create your models here

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=50)
    data_save_accepted = models.BooleanField()
    data_accepted_at = models.DateTimeField(default=timezone.now)
