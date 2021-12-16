# Generated by Django 3.2.7 on 2021-11-13 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0007_auto_20211112_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskweight',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='task_weight', to='auth.user'),
            preserve_default=False,
        ),
    ]