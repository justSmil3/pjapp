from django.db.models.lookups import Contains, Range
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import \
    TrackSerializer, TaskSerializer, SubtaskSerializer, UserSerializer, TaskWeightSerializer, TokenSerializer, StatsSerializer
from rest_framework import status
from .models import Task, SubTask, Track, TaskWeight, Stats
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from knox.models import AuthToken

from api import serializers


@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exeption=ValueError):
        serializer.create(validated_data=request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({
        'error': True,
        'error_msg': serializer.error_messages,
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(request, username = username, password = password)
    serializer = UserSerializer(user, many=False)
    if user is not None:
        t = login(request, user)
        token = AuthToken.objects.create(user)
        return Response({"token": AuthToken.objects.create(user)[1]})
    return Response({
        'error': True,
        'error_msg': serializer.error_messages,
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def logout_user(request):
    logout(request)
    return Response()



@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/tracks/',
            'method': 'GET',
            'body': None, 
            'description': 'Returns an array of tracks'
        },
        {
            'Endpoint': '/tracks/id',
            'method': 'GET',
            'body': None, 
            'description': 'Returns a single track object '
        },
        {
            'Endpoint': '/tracks/create/',
            'method': 'POST',
            'body': {'body': ""}, 
            'description': 'creates new track with data sent in post request'
        },
        {
            'Endpoint': '/tracks/id/update/',
            'method': 'PUT',
            'body': {'body': ""}, 
            'description': 'creates an existing track with data sent in put request'
        },
        {
            'Endpoint': '/tracks/id/delete/',
            'method': 'DELETE',
            'body': None, 
            'description': 'deletes an existing track '
        },
        #TODO no api_view jet
        {
            'Endpoint': '/tasks/',
            'method': 'GET',
            'body': None, 
            'description': 'Returns an array of tasks'
        },
        {
            'Endpoint': '/tasks/id',
            'method': 'GET',
            'body': None, 
            'description': 'Returns a single task object '
        },
        {
            'Endpoint': '/subtasks/',
            'method': 'GET',
            'body': None, 
            'description': 'Returns an array of subtasks'
        },
        {
            'Endpoint': '/subtasks/id',
            'method': 'GET',
            'body': None, 
            'description': 'Returns a single subtask object '
        },
        {
            'Endpoint': '/osubtasks/sort',
            'method': 'GET',
            'body': None, 
            'description': 'Returns a single subtask object '
        },
        {
            'Endpoint': '/weights/',
            'method': 'GET',
            'body': {'body': ""},
            'description': 'Returns all weights / wheighted tasks for a user'
        },
        {
            'Endpoint': '/weights/count',
            'method': 'GET',
            'body': {'body': ""},
            'description': 'Returns a certain number of weights / wheighted tasks for a user'
        },
        {
            'Endpoint': '/stats/count', 
            'method': 'GET', 
            'body': {'body': ""},
            'description': 'returns the stats for a user'
        },
        {
            'Endpoint': '/addweightscore/', 
            'method': 'POST', 
            'body': {'body': ""},
            'description': 'returns the stats for a user'
        }
    ]
    return Response(routes)

@api_view(['GET'])
def getTasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTask(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)



@api_view(['GET'])
def getSubtasks(request):
    subtasks = SubTask.objects.all()
    serializer = SubtaskSerializer(subtasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getOSubtasks(request, pk):
    subtasks = SubTask.objects.all().order_by("-"+pk)
    serializer = SubtaskSerializer(subtasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSubtask(request, pk):
    subtask = SubTask.objects.get(id=pk)
    serializer = SubtaskSerializer(subtask, many=False)
    return Response(serializer.data)



@api_view(['GET'])
def getTracks(request):
    tracks = request.user.tracks.all()
    serializer = TrackSerializer(tracks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTrack(request, pk):
    track = request.user.tracks.get(id=pk)
    serializer = TrackSerializer(track, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def createTrack(request):
    data = request.data
    #Todo
    track = Track.objects.create(
        task=SubTask.objects.get(name=data["task"]),
        rating_0=data["rating_0"],
        rating_1=data["rating_1"],
        user=request.user, 
    )
    serializer = TrackSerializer(track, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateTrack(request, pk):
    data = request.data
    track = Track.objects.get(id=pk)

    serializer = TrackSerializer(track, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def deleteTrack(request, pk):
    track = Track.objects.get(id=pk)
    track.delete()
    return Response('tracking was deleted!')

@api_view(['GET'])
def getWeights(request):
    weights = request.user.task_weight.all();
    serializer = TaskWeightSerializer(weights, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getCountedWeights(request, count):
    weights = request.user.task_weight.filter().order_by("-weight")[:count]
    serializer = TaskWeightSerializer(weights, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteWeight(request, pk):
    weight = TaskWeight.objects.get(id=pk)
    weight.delete()
    return Response('weighting was deleted')

@api_view(['POST'])
def addWeightScore(request):
    data = request.data
    track = request.user.tracks.get(id=data["track"])
    track.score += int(data["score"])
    track.save()
    return Response(track.score)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def getStats(request, count):
    # tracks = request.user.tracks.filter().order_by("created")
    tracks = request.user.tracks.filter().order_by("created")
    dates = [] 
    for i in tracks:
         if(len(dates) < 5):
             if not dates.__contains__(i.created.date()):
                    dates.append(i.created.date())
    
    statlist = []
    
    weights = TaskWeight.objects.all()
    usedWeights = []
    for i in dates:
        score = 0
        for track in tracks:
            if track.created.date() == i:
                 score += track.score
                 print(track.score)
            
        stats = Stats.objects.create(
        date = i,
        score = score
        );
        statlist.append(stats)
    serializer = StatsSerializer(statlist, many=True)
    return Response(serializer.data)