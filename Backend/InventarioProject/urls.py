"""InventarioProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from InventarioApp import views

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('user/', views.UserCreateView.as_view()),
    path('user/<int:pk>/', views.UserDetailView.as_view()),
    path('userUpdate/<int:pk>/', views.UserUpdateView.as_view()),
    path('itemCreate/', views.ItemCreateView.as_view()),
    path('itemDelate/<int:pk>/<int:user>/', views.ItemDeleteView.as_view()),
    path('itemUpdate/<int:pk>/<int:user>/', views.ItemUpdateView.as_view()),
    path('item/<int:pk>/<int:user>/', views.ItemDetailView.as_view()),
    path('itemListView/<int:user>/', views.ItemListView.as_view()),
    path('transactionCreate/<int:user>/', views.TransactionCreateView.as_view()),
    path('transaction/<int:pk>/<int:user>/', views.TransactionDetailView.as_view()),
    path('transactionByItemList/<int:item>/<int:user>/', views.TransactionByItemListView.as_view()),
]
