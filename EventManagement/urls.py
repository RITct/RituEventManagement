from django.contrib.auth import views as auth_views

from django.urls import path
from django.views.generic import TemplateView

from EventManagement import views
urlpatterns = [
    path('', views.index, name="index"),
    path('admin_panel', views.admin_panel, name="admin_panel"),
    path('add/profile',views.add_profile, name="add_profile"),
    path('add/profile/success', TemplateView.as_view(template_name='EventManagement/profile_add_sucess.html'), name="add_profile_success"),
    path('update/event/<slug:event_code', views.UpdateEvent.as_view, name="update_event"),
    path('login', auth_views.login, name="login"),
    path('logout', auth_views.logout, name="logout"),


    path('api/get/event/data', views.get_event_data, name="get_event_data"),
    path('api/get/user/data', views.get_user_data, name="get_user_data"),
]