from django.contrib import admin
from .models import Task, SubTask, Track, TaskWeight, Message, Menti#, ExtraData

# Register your models here.

admin.site.register(Task)
admin.site.register(Track)
admin.site.register(SubTask)
admin.site.register(TaskWeight)
admin.site.register(Message)
admin.site.register(Menti)
# admin.site.register(ExtraData)

