# Generated by Django 3.0.4 on 2020-07-17 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userData', '0008_auto_20200308_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bargain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver', models.CharField(max_length=100)),
                ('customer', models.CharField(max_length=100)),
                ('bargain', models.TextField(default='[]')),
            ],
        ),
        migrations.AlterField(
            model_name='userdetailsinfo',
            name='isDriver',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
