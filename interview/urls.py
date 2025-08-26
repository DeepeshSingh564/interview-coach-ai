
from django.urls import path
from . import views


urlpatterns =[
  path('', views.home, name='home'),
  path('api/roles', views.api_roles, name='api_roles'),
  path('api/question', views.api_question, name='api_question'),
  path('api/answer', views.api_answer, name='api_answer'),
  
]