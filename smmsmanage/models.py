from django.db import models

# Create your models here.

class ImageList(models.Model):
    filename = models.CharField(max_length=100)
    fileurl = models.CharField(max_length=1024)
    size = models.CharField(max_length=20)
    width = models.CharField(max_length=20)
    height = models.CharField(max_length=20)
    uploaddate = models.TimeField()
    deleteurl = models.CharField(max_length=1024)

    class Meta:
        ordering = ('-uploaddate',)

    def __str__(self):
        return self.filename

