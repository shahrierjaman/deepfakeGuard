from django.urls import path
from . import views

urlpatterns = [
    # General User URLs
    path('', views.index, name='index'),  
    path('upload-media/', views.upload_media, name='upload_media'),
    path('notifications/', views.notifications, name='notification'),
    path('flag-content/', views.flag_content, name='flag_content'),
    path('upload-report/', views.flag_content, name='upload_report'),
    path('analysis-history/', views.analysis_history, name='analysis_history'),
    path('settings/', views.settings, name='settings'),

    # Investigator URLs
    path('investigator-dashboard/', views.investigator_dashboard, name='investigator_dashboard'),
    path('case-management/', views.case_management, name='case_management'),
    path('deepfake-analysis/', views.deepfake_analysis, name='deepfake_analysis'),

    # Administrator URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user-management/', views.user_management, name='user_management'),
    path('system-analysis/', views.system_analysis, name='system_analysis'),
    path('flagged-content/', views.flagged_content, name='flagged_content'),
]