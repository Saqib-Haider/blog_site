from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from . import views
from .views import (PDetailView, PCreateView, PUpdateView, PDeleteView, PostList, PostDetail)

urlpatterns = [
    path('api/',PostList.as_view(), name='list&create'),
    path('api/<int:id>/',PostDetail.as_view(), name='deelete%update'),
    path('',views.home, name='home'),
    path('registration/',views.registration, name='regis_url'),
    path('login/',LoginView.as_view(), name='login_url'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('list/',views.list, name='list'),
    path('list/create/',views.create, name='createpost'),
    #path('create/', views.create, name='create'),
    path('create/', PCreateView.as_view(), name='create'),
    #path('detail/<slug:slug>/',views.detail, name='detail'),
    path('detail/<slug:slug>/', PDetailView.as_view(), name='detail'),
    #path('detail/<slug:slug>/edit/',views.update, name='update'),
    path('detail/<slug:slug>/edit/',PUpdateView.as_view(), name='update'),
    #path('detail/<slug:slug>/delete/',views.delete, name='delete'),
    path('detail/<slug:slug>/delete/', PDeleteView.as_view(), name='delete'),

]