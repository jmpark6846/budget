# Generated by Django 2.1.3 on 2018-11-07 02:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budget', '0003_budget_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='예산')),
                ('amount', models.IntegerField(verbose_name='금액')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성날짜')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='수정날짜')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
        ),
        migrations.CreateModel(
            name='BudgetItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_in_budget', models.IntegerField(verbose_name='금액')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budget_items', to='budget.BudgetCategory', verbose_name='예산 카테고리')),
            ],
        ),
        migrations.RemoveField(
            model_name='budget',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='budget',
            name='created',
        ),
        migrations.RemoveField(
            model_name='budget',
            name='name',
        ),
        migrations.RemoveField(
            model_name='budget',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='budget',
            name='user',
        ),
        migrations.AddField(
            model_name='budget',
            name='month',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='월'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='budget',
            name='items',
            field=models.ManyToManyField(related_name='budgets', to='budget.BudgetItem'),
        ),
    ]