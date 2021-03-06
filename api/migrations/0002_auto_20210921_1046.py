# Generated by Django 3.2.7 on 2021-09-21 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.TextField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_0', models.CharField(choices=[('0', 'keine ausführrung'), ('1', 'gemeinsam mit dem Arzt'), ('2', 'unter Beobachtung des Arztes'), ('3', 'eigenständig, Alles/Vieles wird nachgeprüft'), ('4', 'eigenständig, Wichtiges wird nachgeprüft'), ('5', 'eigenständig, Wichtiges wird telefonisch nachgeprüft')], default='0', max_length=1)),
                ('rating_1', models.CharField(choices=[('0', 'keine ausführrung'), ('1', 'gemeinsam mit dem Arzt'), ('2', 'unter Beobachtung des Arztes'), ('3', 'eigenständig, Alles/Vieles wird nachgeprüft'), ('4', 'eigenständig, Wichtiges wird nachgeprüft'), ('5', 'eigenständig, Wichtiges wird telefonisch nachgeprüft')], default='0', max_length=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='track', to='api.subtask')),
            ],
            options={
                'ordering': ['-updated'],
            },
        ),
        migrations.DeleteModel(
            name='Note',
        ),
        migrations.AddField(
            model_name='subtask',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtask', to='api.task'),
        ),
    ]
