from django.urls import path
from .views import *
urlpatterns = [
    path('create/', Todo_list, name='create')
]
