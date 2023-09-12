from django.urls import path
from . import views

urlpatterns = [
    path('displayData/', views.mainDataTable, name="mainDataTable"),
]