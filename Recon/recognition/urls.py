from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path('', views.index, name= 'home'),
    path('select_image/',views.recognize,name='select_image'),
    
    path("recognize/", views.recognize, name="recognize"),
    #path('scan/',views.scan,name='scan'),
    

]