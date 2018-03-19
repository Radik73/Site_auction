from django.urls import path
from . import views


urlpatterns = [
    path('lots/', views.give_lots, name='lots')
]