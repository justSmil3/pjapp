from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    name = models.TextField()
    description = models.TextField()
    parent = models.ForeignKey("Task", blank=True, related_name="child", null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name[0:50]



class SubTask(models.Model):
    task = models.ForeignKey(Task, related_name='subtask', on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    scoreadd = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class TaskWeight(models.Model):
    weight = models.IntegerField()
    task = models.ForeignKey(SubTask, related_name="weight", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="task_weight", on_delete=models.CASCADE)

class Track(models.Model):
    # TODO reconsider naming
    class Reviews(models.TextChoices):
        KEINE_AUSFÜHRUNG = '0', 'keine ausführrung'
        GEMEINSAM_MIT_DEM_ARZT = '1', 'gemeinsam mit dem Arzt'
        UNTER_BEOBACHTUNG_DES_ARZTES = '2', 'unter Beobachtung des Arztes'
        EIGENSTÄNDIG_VIELES_WIRD_NACHGEPRÜFT  = '3', 'eigenständig, Alles/Vieles wird nachgeprüft'
        EIGENSTÄNDIG_WICHTIGES_WIRD_NACHGEPRÜFT = '4', 'eigenständig, Wichtiges wird nachgeprüft'
        EIGENSTÄNDIG_WICHTIGES_WIRD_TELEFONISCH_NACHGEPRÜFT = '5', 'eigenständig, Wichtiges wird telefonisch nachgeprüft'

    task = models.ForeignKey(SubTask, related_name='track', on_delete=models.PROTECT)
    rating_0 = models.CharField(
        max_length=1,
        choices=Reviews.choices,
        default=Reviews.KEINE_AUSFÜHRUNG,
    )
    rating_1 = models.CharField(
        max_length=1,
        choices=Reviews.choices,
        default=Reviews.KEINE_AUSFÜHRUNG,
    )
    user = models.ForeignKey(User, related_name='tracks', on_delete=models.CASCADE)
    score = models.IntegerField(default=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.task.name
    class Meta:
        ordering = ['-updated']
        
class Stats(models.Model):
    date = models.DateField()
    score = models.IntegerField()
    
    def __str__(self): 
        return self.date
    