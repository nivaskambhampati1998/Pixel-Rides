# Generated by Django 3.0.4 on 2020-07-20 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userData', '0010_delete_bargain'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scheduled_Rides',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=50)),
                ('source', models.CharField(default='', max_length=50)),
                ('destination', models.CharField(default='', max_length=50)),
                ('dateTime', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
