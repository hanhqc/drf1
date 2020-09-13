from django.urls import path

from app2 import views

urlpatterns = [
    path('stu/', views.Student.as_view()),
]
