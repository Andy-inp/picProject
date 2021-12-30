from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    token = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=30, blank=True)
    disk_usage = models.CharField(max_length=50, blank=True)
    disk_usage_raw = models.IntegerField(null=True)
    disk_limit = models.CharField(max_length=50, blank=True)
    disk_limit_raw = models.IntegerField(null=True)
    last_requestid = models.CharField(max_length=50, blank=True)
    usage_percent = models.FloatField(null=True)
    # userforein = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"username {self.username}"

