from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Abteilungen(models.TextChoices):
    Generel = '0', 'ALL'
    Augenheilkunde = '1', 'AUGENHEILKUNDE'

class ExtraData(models.Model):
    user = models.ForeignKey(User, related_name='extra_data', on_delete=models.CASCADE)
    abteil = models.CharField(
        max_length=1,
        choices=Abteilungen.choices,
        default=Abteilungen.Generel,
    )
    def __str__(self):
        return self.user.username
    

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
    classes = models.TextField(default="ALL")
    
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
        EIGENSTÄNDIG  = '3', 'eigenständig'

    task = models.ForeignKey(SubTask, related_name='track', on_delete=models.PROTECT)
    rating_0 = models.CharField(
        max_length=1,
        choices=Reviews.choices,
        default=Reviews.KEINE_AUSFÜHRUNG,
    )
    rating_1 = models.FloatField()
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
    
class Message(models.Model):
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name="created_messages", on_delete=models.CASCADE)
    Message = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    
class Menti(models.Model):
    mentor = models.ForeignKey(User, related_name="menti", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name= "mentor", on_delete=models.CASCADE)
    name = models.TextField(default="")
    visable = models.BooleanField(default=True)
    
    def __str__(self): 
        return f"mentor: {mentor.username}; menti: {user.username}"