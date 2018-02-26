from django.urls import path

from EventManagement import views
urlpatterns = [
    path('', views.index, name="index"),
    path('admin_panel', views.admin_panel, name="admin_panel"),
    path('add/event/volunteer', views.head_event_volunteer_add, name="add_event_volunteer"),
    path('add/profile',views.add_profile, name="add_profile"),
]