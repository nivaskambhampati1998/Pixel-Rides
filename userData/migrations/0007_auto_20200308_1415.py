# Generated by Django 3.0.2 on 2020-03-08 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userData', '0006_wallethistory_walletmapping'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallethistory',
            name='sid',
        ),
        migrations.AlterField(
            model_name='wallethistory',
            name='amount',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='wallethistory',
            name='date',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='wallethistory',
            name='receiver',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='walletmapping',
            name='password',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='walletmapping',
            name='private',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='walletmapping',
            name='public',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]
