# Generated by Django 2.1.3 on 2018-11-08 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0006_auto_20181107_1228'),
    ]

    operations = [
        migrations.RenameField(
            model_name='budgetitem',
            old_name='amount_in_budget',
            new_name='spent',
        ),
    ]