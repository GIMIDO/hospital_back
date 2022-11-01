from django.urls import path
from .views import *

urlpatterns = [
    path('customer/', CustomerView.as_view()),
    path('customer/<int:num>', CustomerView.as_view()),
    path('department/', DepartmentView.as_view()),
    path('department/<int:num>', DepartmentView.as_view()),
    path('employee/', EmployeeView.as_view()),
    path('employee/<int:num>', EmployeeView.as_view()),
    path('appointment/', AppointmentView.as_view()),
    path('appointment/<int:num>', AppointmentView.as_view()),
    path('login/', LoginView.as_view()),
    path('login/<str:token>', LoginView.as_view())
]
