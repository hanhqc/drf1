from django.urls import path

from app1 import views

urlpatterns = [
    path('user/', views.user),
    path('user2/', views.UserView.as_view()),
    path('emp/', views.Employee.as_view()),
    path('emp/<str:id>/', views.Employee.as_view()),
    path('stu/', views.Student.as_view()),
    path('stu/<str:id>/<str:name>/<str:pwd>/', views.Student.as_view()),
]
