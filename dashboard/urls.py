from django.urls import path
from . import views
from website import views as website_views

urlpatterns = [
    path('crm/', views.home, name='home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('agent-dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('team/', website_views.team_manage, name='team_manage'),
    path('team/add/', website_views.team_member_edit, name='team_member_add'),
    path('team/<int:pk>/edit/', website_views.team_member_edit, name='team_member_edit'),
    path('team/<int:pk>/delete/', website_views.team_member_delete, name='team_member_delete'),
]
