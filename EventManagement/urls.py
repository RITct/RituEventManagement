from django.contrib.auth import views as auth_views

from django.urls import path

from EventManagement import views
urlpatterns = [
    path('', views.index, name="index"),
    path('admin_panel', views.admin_panel, name="admin_panel"),
    path('add/profile',views.add_profile, name="add_profile"),
    path('login', auth_views.login, name="login"),
    path('logout', auth_views.logout, name="logout"),


    path('api/get/event/data', views.get_event_data, name="get_event_data"),
    path('api/get/user/data', views.get_user_data, name="get_user_data"),
]