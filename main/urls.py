from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('profile/<str:pk>/', views.userProfile, name="profile"),
    path('profile_edit/', views.updateUser, name="profile_edit"),

    path('post/<str:pk>/', views.postPage, name="post"),
    path('create-post/', views.createPost, name="create-post"),
    path('update-post/<str:pk>/', views.updatePost, name="update-post"),
    path('delete-post/<str:pk>/', views.deletePost, name="delete-post"),

    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('topics/', views.topicsPage, name="topics")
]
