from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('lots/', views.give_lots, name='lots'),
    path('lot_detail/<pk>', views.lot_detail, name='lot_detail'),
    path('make_rate/<pk>', login_required(views.make_rate), name='make_rate'),
    # path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]