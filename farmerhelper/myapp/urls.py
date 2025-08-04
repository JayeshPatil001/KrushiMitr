from django.contrib import admin
from django.urls import path,include
from myapp import views

urlpatterns = [
    path('',views.user_login,name='login'),
    path('register/',views.user_register,name='register'),
    path('home/',views.home,name='home'),
    path('logout/',views.user_logout,name='logout'),
    path('inquiry/',views.user_inquiry,name='inquiry'),
    path('add_harvest/',views.add_harvest,name='harvest'),
    path('add_crop/',views.add_crop,name='crop'),
    path('add_expense/',views.add_expense,name='expense'),
    path('history/',views.history,name='history'),
    path('harvest_history/',views.harvest_history,name='harvest_history'),
    path('expense_history/',views.expense_history,name='expense_history'),
]
