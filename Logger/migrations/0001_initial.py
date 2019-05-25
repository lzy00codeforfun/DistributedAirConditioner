# Generated by Django 2.1.7 on 2019-05-25 02:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RunLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currenttime', models.DateTimeField(default=django.utils.timezone.now)),
                ('roomid', models.CharField(max_length=20)),
                ('temperature', models.FloatField()),
                ('windspeed', models.IntegerField()),
                ('status', models.CharField(max_length=20)),
                ('logtype', models.CharField(max_length=20)),
                ('flag', models.CharField(max_length=30)),
            ],
        ),
    ]
