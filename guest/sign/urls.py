from django.urls import path
from sign import views_api

urlpatterns = [

    path('add_event/', views_api.add_event),
]