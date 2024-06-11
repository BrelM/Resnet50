from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path('', views.index, name= 'home'),
    path('select_image/',views.recognize,name='select_image'),
    path('voters/',views.voters,name='voters'),
    path("recognize/", views.recognize, name="recognize"),
    #path('nom/<int:nom_id>/', views.nom_detail, name='detail'),
]
    #path('voter/<str:label>/', views.voter, name='voter'),
    #path('scan/',views.scan,name='scan'),
    

