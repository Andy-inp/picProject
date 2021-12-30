# Generated by Django 3.2.9 on 2021-12-30 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='disk_limit',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='disk_limit_raw',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='disk_usage',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_requestid',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
