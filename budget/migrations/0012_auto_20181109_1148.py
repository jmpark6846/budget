# Generated by Django 2.1.3 on 2018-11-09 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0011_auto_20181109_1135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budget',
            name='month',
        ),
        migrations.RemoveField(
            model_name='budget',
            name='year',
        ),
    ]