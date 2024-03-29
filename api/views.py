##################################################################################################################################
# In diesem file sind alle funktionen definiert, welche per API request angesteuert werden können.
# Es gibt mehrere arten so eine funktion zu definieren. Die hier verwendete ist über den decorator api_view,
# der einen parameter nimmt der entweder GET, POST oder PUT ist. GET beschreibt eine funktion die daten von der 
# datenbank abgreift. POST beschreibt eine funktion die daten auf die datenbank schiebt / "posted".
# PUT beschreibt eine funktion die daten auf der datenbank mit neuen daten aus der request updated.
# eine funktion benötigt als parameter immer die request selber, naming convention ist dabei diesen parameter request zu nennen.
# daten können als json in einer api request mit gesendet werden. man kan über den handler request.data auf diese json zugreifen
# und dann wie in einem dictionary auf diese daten zugreifen, als beispiel: 
# json file: 
# {
#  "example": "1234",   
# }
# print(request.data["example"]) prints out 1234.
# 
# eine api funktion muss als return eine Response zurücksenden, die data im json format sowie einen http status sowie zum beispiel 
# den status 400, bad request tragen kann.
#################################################################################################################################

from django.db.models.lookups import Contains, Range
from django.db.models.query_utils import subclasses
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import \
    MentiSerializer, TrackSerializer, TaskSerializer, SubtaskSerializer, UserSerializer, TaskWeightSerializer, TokenSerializer, StatsSerializer, MessageSerializer, \
    MentiSerializer
from rest_framework import status
from .models import ExtraData, Message, Task, SubTask, Track, TaskWeight, Stats, Message, Menti, Abteilungen
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from knox.models import AuthToken
from django.core.mail import send_mail
import json
from datetime import date, datetime

from api import serializers

users_to_change = []
currentdate = -1;

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
    username = username.lower()
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

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def forgot_password(request):
    global currentdate
    tmpdate = datetime.today().day
    if not currentdate == tmpdate:
        users_to_change.clear()
        currentdate = tmpdate
    loginname = request.data['name'].lower()
    user = None
    code = request.data['code'];
    try:
        user = User.objects.get(email=loginname)
    except:
        try:
            user = User.objects.get(username=loginname)
            
        except:
            return Response({
                    'error': True,
                    'error_msg': "did not find user",
                    }, status=status.HTTP_400_BAD_REQUEST)
    tmpuser = authenticate(request, username = "resetPasswordUser", password = "a4dfjlasd4jfa345sduf35sdhf")
    t = login(request, tmpuser)
    token = AuthToken.objects.create(tmpuser)
    users_to_change.append(user)
    send_mail(
    'Forgot Password',
    f'Dein Passwort reset code ist {code}',
    'PjAppMainz@gmail.com',
    [user.email],
    fail_silently=False,
    )
    return Response({"token": AuthToken.objects.create(tmpuser)[1], "name": user.username})

@api_view(['POST']) # TODO URGENT this is a huge security risk
def reset_password(request):
    global currentdate
    tmpdate = datetime.today().day
    if not currentdate == tmpdate:
        users_to_change.clear()
        currentdate = tmpdate
    loginname = request.data['name'].lower()
    password = request.data['password']
    user = User.objects.get(username=loginname)
    if user in users_to_change:
        user.set_password(password)
        user.save()
        users_to_change.remove(user)
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
def getAllSubtasks(request):
    subtasks = SubTask.objects.all()
    serializer = SubtaskSerializer(subtasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSubtasks(request):
    try:
        ed = request.user.extra_data.get()
    except:
        ed = ExtraData.objects.create(
            user=request.user, 
        )
        
    subtasks = SubTask.objects.all().filter(classes=1)
    userclass = ed.abteil
    
    subtasks = subtasks | SubTask.objects.all().filter(classes = userclass)
    subtasks = subtasks.order_by("task")
    serializer = SubtaskSerializer(subtasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getMentiSubtasks(request, pk):
    try:
        ed = User.objects.get(id=pk).extra_data.get()
    except:
        ed = ExtraData.objects.create(
            user=User.objects.get(id=pk), 
        )
        
        
    #print(ed.get_abteil_display())
    subtasks = SubTask.objects.all().filter(classes=1)
    userclass = ed.abteil
    
    subtasks = subtasks | SubTask.objects.all().filter(classes = userclass)
    subtasks = subtasks.order_by("task")
    serializer = SubtaskSerializer(subtasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSubtasksByTask(request, pk):
    task = Task.objects.get(id=pk);
    subtasks = task.subtask.all();
    serializer = SubtaskSerializer(subtasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSubtasksOrderedByTask(request):
    subtasks = SubTask.objects.all().order_by("task")
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
def getMentiTracks(request, pk):
    user = User.objects.get(id = pk)
    tracks = user.tracks.all()
    serializer = TrackSerializer(tracks, many=True)
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

@api_view(['GET'])
def getTrackOnTask(request, pk):
    
    try:
        track = request.user.tracks.get(task=SubTask.objects.get(id=pk))
        serializer = TrackSerializer(track, many=False)
        return Response(serializer.data)
    
    except Exception as e:
        return Response({
        'error': True,
        'error_msg': str(e)
        })

@api_view(['POST'])
def createTrack(request):
    data = request.data
    task = SubTask.objects.get(name=data["task"])
    try:
        track = Track.objects.filter(task=task).get(user=request.user)
        track.rating_0=data["rating_0"]
        track.rating_1=data["rating_1"]
        track.save(update_fields=["rating_0", "rating_1"])
        # serializer = TrackSerializer(track, data=request.data)
        # if serializer.is_valid():
        #     print("hi")
        #     serializer.save()
        # print(str(serializer.errors))
    except:
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
def getWeightOnTask(request, mentiID, taskID):
    
    try:
        user = User.objects.get(id=mentiID);
        weight = user.task_weight.get(task=SubTask.objects.get(id=taskID));
        serializer = TaskWeightSerializer(weight, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({
        'error': True,
        'error_msg': str(e)
        })

@api_view(['PUT'])
def updateWeight(request, pk):
    data = request.data
    weight = TaskWeight.objects.get(id=pk)

    serializer = TaskWeightSerializer(weight, data=data)
    if serializer.is_valid():
        serializer.save()

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
def getStats(request, count):
    # tracks = request.user.tracks.filter().order_by("created")
    tracks = request.user.tracks.filter().order_by("-created")
    dates = [] 
    for i in tracks:
         if(len(dates) < count):
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
    statlist.reverse()
    serializer = StatsSerializer(statlist, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUnweightedStats(request, pk, count):
    # tracks = request.user.tracks.filter().order_by("created")
    tracks = User.objects.get(id=pk).tracks.filter().order_by("-created")
    dates = [] 
    for i in tracks:
         if(len(dates) < count):
             if not dates.__contains__(i.created.date()):
                    dates.append(i.created.date())
    
    statlist = []
    
    weights = TaskWeight.objects.all()
    usedWeights = []
    for i in dates:
        score = 0
        for track in tracks:
            if track.created.date() == i:
                if track.score > 2:
                    score += 1
            
        stats = Stats.objects.create(
        date = i,
        score = score
        );
        statlist.append(stats)
    statlist.reverse()
    serializer = StatsSerializer(statlist, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getWeightedStats(request, pk, count):
    # tracks = request.user.tracks.filter().order_by("created")
    tracks = User.objects.get(id=pk).tracks.filter().order_by("-created")
    dates = [] 
    for i in tracks:
         if(len(dates) < count):
             if not dates.__contains__(i.created.date()):
                    dates.append(i.created.date())
    
    statlist = []
    
    weights = TaskWeight.objects.all()
    usedWeights = []
    for i in dates:
        score = 0
        for track in tracks:
            if track.created.date() == i:
                if track.score == 2:
                    score += 1
            
        stats = Stats.objects.create(
        date = i,
        score = score
        );
        statlist.append(stats)
    statlist.reverse()
    serializer = StatsSerializer(statlist, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUnweightedUserStats(request, count):
    tracks = request.user.tracks.filter().order_by("-created")
    dates = [] 
    for i in tracks:
         if(len(dates) < count):
             if not dates.__contains__(i.created.date()):
                    dates.append(i.created.date())
    
    statlist = []
    
    weights = TaskWeight.objects.all()
    usedWeights = []
    for i in dates:
        score = 0
        for track in tracks:
            if track.created.date() == i:
                if track.score > 2:
                    score += 1
            
        stats = Stats.objects.create(
        date = i,
        score = score
        );
        statlist.append(stats)
    statlist.reverse()
    serializer = StatsSerializer(statlist, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getWeightedUserStats(request, count):
    tracks = request.user.tracks.filter().order_by("-created")
    dates = [] 
    for i in tracks:
         if(len(dates) < count):
             if not dates.__contains__(i.created.date()):
                    dates.append(i.created.date())
    
    statlist = []
    
    weights = TaskWeight.objects.all()
    usedWeights = []
    for i in dates:
        score = 0
        for track in tracks:
            if track.created.date() == i:
                if track.score == 2:
                    score += 1
            
        stats = Stats.objects.create(
        date = i,
        score = score
        );
        statlist.append(stats)
    statlist.reverse()
    serializer = StatsSerializer(statlist, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUserStats(request, pk, count):
    # tracks = request.user.tracks.filter().order_by("created")
    tracks = User.objects.get(id=pk).tracks.filter().order_by("-created")
    dates = [] 
    for i in tracks:
         if(len(dates) < count):
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
    statlist.reverse()
    serializer = StatsSerializer(statlist, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createMessage(request):
    message = request.data['message']
    creator = request.user
    user = User.objects.get(id=request.data["user"])
    
    message_object = Message.objects.create(
        Message = message,
        user = user,
        creator = creator
    )
    
    serializer = MessageSerializer(message_object, many=False)
    
    return Response(serializer.data)

@api_view(['GET'])
def getMessage(request, start, count):
    request.user.messages.all().update(read=True);
    mentor = Menti.objects.get(user=request.user).mentor
    message = request.user.messages.all().filter(creator=mentor) | request.user.created_messages.all()
    if count + start > len(message):
        count = len(message) - start
        if count <= 0: 
            return Response(json.dumps({'res1': len(message), 'res2': len(Message.objects.all())}),
                       content_type="application/json")
    returnmessages = message.order_by("-created")[start:count+start]
    serializer = MessageSerializer(returnmessages, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def getUnreadMessagesCount(request, pk):
    messages = User.objects.get(id=pk).created_messages.all().filter(read=False)
    return Response(json.dumps({'count': len(messages)}),
                       content_type="application/json")

@api_view(['GET'])
def getUserSpecificMessage(request, mentiId, start, count):
    # make sure to change that in the case that the user gets more than one mentor.
    User.objects.get(id=mentiId).created_messages.all().update(read=True);
    message = User.objects.get(id=mentiId).created_messages.all() | request.user.created_messages.filter(user = User.objects.get(id=mentiId))
    if count + start > len(message):
        count = len(message) - start
        if count <= 0: 
            return Response()
    returnmessages = message.order_by("-created")[start:count+start]
    serializer = MessageSerializer(returnmessages, many=True)
    
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteMessage(request, pk):
    message = request.user.messages.get(id=pk)
    if not message == None:
        message.delete()
        return('message was deleted successfully')
    else:
        return('message does not exist for user')
    
@api_view(['GET'])
def getMenti(request):
    menti = request.user.menti.all().filter(visable=True)
    for x in menti:
        x.name = x.user.username
    serializer = MentiSerializer(menti, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createTaskWeight(request):
    data = request.data
    task = SubTask.objects.get(id = data["task"])
    try:
        weight = TaskWeight.objects.get(task=task)
        serializer = TaskWeightSerializer(weight, data=data)
        if serializer.is_valid():
            serializer.save()
    except:
        weight = TaskWeight.objects.create(
            weight = int(data['weight']),
            task = task,
            user = User.objects.get(id = data["user"])
        )
        serializer = TaskWeightSerializer(weight, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getTaskWeightsOfUser(request, pk):
    user = User.objects.get(id = pk)
    weights = user.task_weight.all()
    serializer = TaskWeightSerializer(weights, many=True)
    return Response(serializer.data)

    
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def checkUserStatus(request):
    user = request.user
    res = "failed"
    if not user.mentor.all():
        res = "mentor"
    elif not user.menti.all():
        res = "menti"
    return Response(json.dumps({'result': res}),
                       content_type="application/json")
    
@api_view(['GET'])
def getMentorId(request):
    mentorid = request.user.mentor.first().mentor.id
    return Response(json.dumps({'result': mentorid}),
                       content_type="application/json")