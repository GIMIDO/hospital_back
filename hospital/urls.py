from django.urls import path
from .views import *

urlpatterns = [
    path('customer/', CustomerView.as_view()),
    path('customer/<int:pk>', CustomerView.as_view()),
    path('department/', DepartmentView.as_view()),
    path('department/<int:pk>', DepartmentView.as_view()),
    path('employee/', EmployeeView.as_view()),
    path('employee/<int:pk>', EmployeeView.as_view()),
    path('appointment/', AppointmentView.as_view()),
    path('appointment/<int:pk>', AppointmentView.as_view()),
    path('login/', LoginView.as_view()),
    path('login/<str:token>', LoginView.as_view())
]
