# Generated by Django 3.0.4 on 2020-04-08 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='reg_date',
        ),
    ]