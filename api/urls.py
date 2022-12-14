##################################################################################################################################
# in diesem fall sind alle urls der api aufgeführt. diese können über die webadresse/[erster path parameter]/ erreicht werden.
# verbunden werden die urls über einen path, welcher die url mit der views funktion verbindet.
# diese urls werden in einem array zusammen geführt und in dem urls.py in der pjapp location zu der gesamten url ansamlung 
# hinzugefügt.
#
# neben dem senden von daten über das json format in dem api call kan man auch variablen über die url selbst versenden. diese können
# in der funktion als input parameter verwendet werden. In der URL definiert man diese variablen über <[datatype(z.b. str)]:[name]>
# und gecalled werden sie dann einfach über das einfügen der value in der url. 
# Beispiel: 
# url definiton : path('subtasks/menti/<str:pk>/',views.getMentiSubtasks)
# call          : webadresse/subtasks/menti/0/       <- this for example gets the subtasks of the menti with id 0 because 0 gets 
#                                                       fed into views.getMentiSubtasks.
##################################################################################################################################



from django.urls import path
from . import views

urlpatterns = [
        path('', views.getRoutes),
        path('tasks/',views.getTasks),
        path('subtasks/',views.getSubtasks),
        path('subtasks/menti/<str:pk>/',views.getMentiSubtasks),
        path('subtasks/all/',views.getAllSubtasks),
        path('subtasksByTask/<str:pk>/', views.getSubtasksByTask),
        path('subtasksOrderedByTask/', views.getSubtasksOrderedByTask),
        path('osubtasks/<str:pk>/', views.getOSubtasks),
        path('tracks/',views.getTracks),
        path('mentiTracks/<str:pk>/',views.getMentiTracks),
        path('tracks/create/', views.createTrack),
        path('tracks/<str:pk>/update/', views.updateTrack),
        path('tracks/<str:pk>/delete/', views.deleteTrack),
        path('tracks/<str:pk>/',views.getTrack),
        path('tracks/byTask/<str:pk>/',views.getTrackOnTask),
        path('tasks/<str:pk>/',views.getTask),
        path('subtasks/<str:pk>/',views.getSubtask),
        path('users/',views.getUsers ),
        path('users/create/', views.createUser),
        path('weights/', views.getWeights),
        path('weights/byTask/<str:mentiID>/<str:taskID>/', views.getWeightOnTask),
        path('weights/<int:count>/', views.getCountedWeights),
        path('weights/<str:pk>/delete/', views.deleteWeight),
        path('weights/<str:pk>/update/', views.updateWeight),
        path('login/', views.login_user),
        path('logout/', views.logout_user),
        path('forgotPassword/', views.forgot_password),
        path('resetPassword/', views.reset_password),
        path('stats/<int:count>/', views.getStats),
        path('stats/<str:pk>/<int:count>/', views.getUserStats),
        path('weightedStats/<str:pk>/<int:count>/', views.getWeightedStats),
        path('unweightedStats/<str:pk>/<int:count>/', views.getUnweightedStats),
        path('weightedUserStats/<int:count>/', views.getWeightedUserStats),
        path('unweightedUserStats/<int:count>/', views.getUnweightedUserStats),
        path('addweightscore/', views.addWeightScore),
        path('messages/<int:start>/<int:count>/', views.getMessage),
        path('messages/<str:pk>/unread/', views.getUnreadMessagesCount),
        path('mentiMessages/<int:mentiId>/<int:start>/<int:count>/', views.getUserSpecificMessage),
        path('messages/add/', views.createMessage),
        path('messages/<str:pk>/delete/', views.deleteMessage),
        path('menti/', views.getMenti),
        path('taskweight/create/', views.createTaskWeight),
        path('taskweights/user/<str:pk>/', views.getTaskWeightsOfUser),
        path('userStatus/', views.checkUserStatus),
        path('mentorid/', views.getMentorId),
]