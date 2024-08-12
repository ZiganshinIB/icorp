from django.urls import path, include
from . import views

app_name = 'company'

urlpatterns = [
    path('employee/create/', views.create_employee, name='create_employee'),
]
