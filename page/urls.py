from . import views
from django.urls import path


urlpatterns = [
    path('get_projects/', views.get_projects),
    path('get_project_details/', views.get_project_details),
    path('create_project/', views.create_project),
    path('get_openid/', views.get_openid),
    path('drop_project/', views.drop_project),
    path('get_basic_info/', views.get_basic_info),
    path('basic_infomation/', views.basic_infomation),
    path('get_user_avatar/', views.get_user_avatar),
    path('attend_project/', views.attend_project),
    path('quit_project/', views.quit_project)
]
