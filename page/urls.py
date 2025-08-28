from . import views
from django.urls import path


urlpatterns = [
    path('get_projects/', views.get_projects),
    path('create_project/', views.create_project),
    path('get_openid/', views.get_openid),
    path('drop_project/', views.drop_project),
    path('whether_login/', views.whether_login)
]
