# Generated by Django 2.1.3 on 2018-11-11 04:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='계정 이름')),
                ('amount', models.IntegerField(verbose_name='금액')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성날짜')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='수정날짜')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
        ),
    ]
