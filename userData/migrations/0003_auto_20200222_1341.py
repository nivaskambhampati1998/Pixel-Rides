# Generated by Django 3.0.2 on 2020-02-22 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userData', '0002_remove_userdetailsinfo_mobilenumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetailsinfo',
            name='user',
        ),
        migrations.AddField(
            model_name='userdetailsinfo',
            name='username',
            field=models.CharField(default='', max_length=50),
        ),
    ]