#############################################################################################################################
# in diesem file werden die tabellen in der datenbank definiert. ein model ist dabei eine tabelle in der datenbank. 
# zum definierem des models definiert man eine classe die models.Model inherited. man kan darauf hin die felder der tabelle 
# definieren als variable welche als model field declariert wird. 
# die function __str__(self): ist hierbei eine function die einen string returned. Bei diesem string handelt es sich um den 
# namen den einzelne instancen in der tabellenansicht im adminpanel tragen.
# 
# nach dem erstellen des models / der tabelle muss noch ein serializer in dem file serializers.py erstellt werden, falls
# man elemente der datei als json im rahmen eines api calls versenden will.
#############################################################################################################################


from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class Abteilungen(models.TextChoices):
#     Generel = 'ALL'
#     Augenheilkunde = 'AUGENHEILKUNDE'
#     RADIOLOGIE = 'RADIOLOGIE'
class Abteilungen(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class ExtraData(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='extra_data', on_delete=models.CASCADE)
    abteil = models.ForeignKey(Abteilungen, related_name='user', on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.user.username + " | " + self.abteil.name
    

class Task(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True)
    parent = models.ForeignKey("Task", blank=True, related_name="child", null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name[0:50]



class SubTask(models.Model):
    task = models.ForeignKey(Task, related_name='subtask', on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField(blank=True)
    scoreadd = models.IntegerField(default=0)
    classes = models.ForeignKey(Abteilungen, related_name='user_abteil', on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.name

class TaskWeight(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    weight = models.IntegerField()
    task = models.ForeignKey(SubTask, related_name="weight", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="task_weight", on_delete=models.CASCADE)

class Track(models.Model):
    created = models.DateTimeField(auto_now_add=True)
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
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    score = models.IntegerField()
    
    def __str__(self): 
        return self.date
    
class Message(models.Model):
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name="created_messages", on_delete=models.CASCADE)
    Message = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
class Menti(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    mentor = models.ForeignKey(User, related_name="menti", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name= "mentor", on_delete=models.CASCADE)
    name = models.TextField(default="")
    visable = models.BooleanField(default=True)
    
    def __str__(self): 
        return self.name