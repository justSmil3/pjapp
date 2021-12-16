from django.urls import path
from . import views

urlpatterns = [
        path('', views.getRoutes),
        path('tasks/',views.getTasks),
        path('subtasks/',views.getSubtasks),
        path('osubtasks/<str:pk>/', views.getOSubtasks),
        path('tracks/',views.getTracks),
        path('tracks/create/', views.createTrack),
        path('tracks/<str:pk>/update/', views.updateTrack),
        path('tracks/<str:pk>/delete/', views.deleteTrack),
        path('tracks/<str:pk>/',views.getTrack),
        path('tasks/<str:pk>/',views.getTask),
        path('subtasks/<str:pk>/',views.getSubtask),
        path('users/',views.getUsers ),
        path('users/create/', views.createUser),
        path('weights/', views.getWeights),
        path('weights/<int:count>/', views.getCountedWeights),
        path('weights/<str:pk>/delete/', views.deleteWeight),
        path('login/', views.login_user),
        path('logout/', views.logout_user),
        path('stats/<int:count>/', views.getStats),
        path('addweightscore/', views.addWeightScore),
]