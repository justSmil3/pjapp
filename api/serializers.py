from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from .models import Track, Task, SubTask, TaskWeight, Stats, Message, Menti
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueTogetherValidator

class TrackSerializer(ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'

class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class SubtaskSerializer(ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'

class TaskWeightSerializer(ModelSerializer):
    class Meta: 
        model = TaskWeight
        fields = '__all__'

class UserSerializer(ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta: 
        model = User
        fields = (
            'username', 
            'first_name',
            'last_name',
            'email',
            'password'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]
    
class StatsSerializer(ModelSerializer):
    class Meta:
        model = Stats
        fields = '__all__'

class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'
        
class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        
class MentiSerializer(ModelSerializer):
    class Meta:
        model = Menti
        fields = '__all__'