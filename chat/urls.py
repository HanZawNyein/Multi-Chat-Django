from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.all_messages, name="all_message"),
    path('private_room/<int:course_id>/', views.all_messages, name='private_room'),
]
