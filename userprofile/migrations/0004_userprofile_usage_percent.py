# Generated by Django 3.2.9 on 2021-12-30 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_userprofile_disk_usage_raw'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='usage_percent',
            field=models.IntegerField(null=True),
        ),
    ]
