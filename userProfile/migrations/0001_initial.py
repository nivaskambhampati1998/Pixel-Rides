# Generated by Django 3.0.2 on 2020-02-25 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserRides',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=50)),
                ('source', models.CharField(default='', max_length=50)),
                ('destination', models.CharField(default='', max_length=50)),
                ('dateTime', models.DateTimeField(max_length=50)),
                ('driverId', models.CharField(blank=True, max_length=50)),
                ('amount', models.CharField(blank=True, max_length=50)),
                ('paymentMethod', models.CharField(blank=True, max_length=50)),
            ],
        ),
    ]
