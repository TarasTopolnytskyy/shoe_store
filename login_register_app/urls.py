from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('home', views.home),
    path('login_page', views.login_page),
    path('login', views.login),
    path('register', views.register),
    path('success', views.success),
    path('log_out', views.log_out),

    #path('shoe/<int:inventory_id', views.shoe),
    #path('user/<int:user_id', views.user_info),
    #path('checkout', views checkout),


]