from django.db import models
from django.utils import timezone
from userprofile.models import UserProfile
from datetime import datetime

class ImageList(models.Model):
    filename = models.CharField(max_length=100)
    imgurl = models.URLField(blank=True)
    size = models.CharField(max_length=20)
    width = models.IntegerField()
    height = models.IntegerField()
    imghash = models.CharField(max_length=50)
    deleteurl = models.URLField(blank=True)
    last_requestid = models.CharField(max_length=50, blank=True)
    # uploaddate = models.DateTimeField(default=datetime.now)
    uploaddate = models.DateTimeField(default=timezone.now)

    belong_user = models.ForeignKey(UserProfile, models.CASCADE)

    class Meta:
        ordering = ('-uploaddate',)

    def __str__(self):
        return self.filename

