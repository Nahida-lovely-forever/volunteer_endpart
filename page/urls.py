from . import views
from django.urls import path


urlpatterns = [
    path('get_projects/', views.get_projects),
    path('create_project/', views.create_project)
]
