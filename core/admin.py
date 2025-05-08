from django.contrib import admin
from .models import User, Case, Finding, Notification, ActivityLog, AnalysisResult, MediaReport

# Register your models here
admin.site.register(User)
admin.site.register(Case)
admin.site.register(Finding)
admin.site.register(Notification)
admin.site.register(ActivityLog)
admin.site.register(AnalysisResult)
admin.site.register(MediaReport)