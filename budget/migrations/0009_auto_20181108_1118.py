# Generated by Django 2.1.3 on 2018-11-08 02:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0008_auto_20181108_1044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budget',
            name='items',
        ),
        migrations.RemoveField(
            model_name='budgetitem',
            name='user',
        ),
        migrations.AddField(
            model_name='budgetitem',
            name='budget',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='budget.Budget', verbose_name='예산'),
            preserve_default=False,
        ),
    ]
