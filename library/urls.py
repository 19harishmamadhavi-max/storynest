from django.urls import path

from . import views


app_name = 'library'

urlpatterns = [
    path('', views.home, name='home'),
    path('stories/<int:story_id>/', views.story_detail, name='story_detail'),
]
