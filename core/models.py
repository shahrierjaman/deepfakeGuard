from django.db import models

   # User model to store General Users, Administrators, and Investigators
class User(models.Model):
       username = models.CharField(max_length=50, unique=True)
       email = models.EmailField(max_length=100)
       password_hash = models.CharField(max_length=255)
       role = models.CharField(max_length=20, choices=[
           ('general', 'General'),
           ('admin', 'Admin'),
           ('investigator', 'Investigator')
       ])
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)

       def __str__(self):
           return self.username

class Case(models.Model):
       file_name = models.CharField(max_length=100)
       file_path = models.CharField(max_length=255)
       flagged_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flagged_cases')
       initial_result = models.CharField(max_length=100)
       description = models.TextField(blank=True)
       priority = models.CharField(
           max_length=20,
           choices=[
               ('high', 'High'),
               ('medium', 'Medium'),
               ('low', 'Low')
           ]
       )
       status = models.CharField(
           max_length=20,
           choices=[
               ('pending', 'Pending'),
               ('assigned', 'Assigned'),
               ('reviewed', 'Reviewed'),
               ('resolved', 'Resolved')
           ]
       )
       assigned_to = models.ForeignKey(
           User,
           on_delete=models.SET_NULL,
           null=True,
           blank=True,
           related_name='assigned_cases'
       )
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)

       def __str__(self):
           return self.file_name

class AnalysisResult(models.Model):
       MEDIA_TYPE_CHOICES = [
           ('image', 'Image'),
           ('video', 'Video'),
       ]
       media_type = models.CharField(max_length=50, choices=MEDIA_TYPE_CHOICES)
       media_file = models.FileField(upload_to='uploads/')
       prediction = models.CharField(max_length=50)
       confidence = models.FloatField()

       def __str__(self):
           return f"{self.media_type} - {self.media_file.name}"

class Finding(models.Model):
       case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='findings')
       investigator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='findings')
       final_determination = models.CharField(max_length=20, choices=[
           ('confirmed-deepfake', 'Confirmed Deepfake'),
           ('authentic', 'Authentic'),
           ('inconclusive', 'Inconclusive')
       ])
       confidence_score = models.FloatField()
       comments = models.TextField(blank=True, null=True)
       submitted_at = models.DateTimeField(auto_now_add=True)

       def __str__(self):
           return f"Finding for {self.case.file_name}"

class Notification(models.Model):
       user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
       case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='notifications')
       message = models.TextField()
       is_read = models.BooleanField(default=False)
       created_at = models.DateTimeField(auto_now_add=True)

       def __str__(self):
           return f"Notification for {self.user.username}"

class ActivityLog(models.Model):
       user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
       case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True, blank=True, related_name='activity_logs')
       action = models.CharField(max_length=100)
       details = models.TextField(blank=True, null=True)
       timestamp = models.DateTimeField(auto_now_add=True)

       def __str__(self):
           return f"{self.action} by {self.user.username}"

class MediaReport(models.Model):
       media = models.ForeignKey('AnalysisResult', on_delete=models.CASCADE)
       reason = models.CharField(max_length=50, choices=[
           ('deepfake', 'Deepfake/Misleading'),
           ('violence', 'Violent Content'),
           ('nudity', 'Nudity/Explicit'),
           ('other', 'Other'),
       ])
       message = models.TextField(blank=True, null=True)
       reported_at = models.DateTimeField(auto_now_add=True)

       def __str__(self):
           return f"Report on {self.media.media_file.name} - {self.reason}"