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

    path('new_item', views.new_item),
    path('user', views.user_info),

    path('create_item', views.create_item),
    path('user/edit', views.edit_user),
    path('update_user', views.update_user),




    path('shoe/<int:inventory_id>', views.item_info),

    path('charge/', views.charge, name='charge'),
    path('', views.HomePageView.as_view(), name='home')
    
    #path('checkout', views checkout),
]