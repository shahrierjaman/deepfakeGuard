from django import forms
from .models import Case, AnalysisResult, MediaReport

class UploadMediaForm(forms.Form):
    MEDIA_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    media_type = forms.ChoiceField(choices=MEDIA_CHOICES, label="Select Media Type")
    media_file = forms.FileField(label="Upload Media")

class FlagContentForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['file_path', 'initial_result', 'description', 'priority']
        widgets = {
            'file_path': forms.URLInput(attrs={'placeholder': 'https://example.com/media'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe why you think this content is suspicious'}),
        }

class MediaReportForm(forms.ModelForm):
    class Meta:
        model = MediaReport
        fields = ['media', 'reason', 'message']
    
    media = forms.ModelChoiceField(
        queryset=AnalysisResult.objects.all(),
        empty_label="Select Media",
        label="Select Media"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['media'].label_from_instance = lambda obj: f"{obj.media_type.capitalize()} - {obj.media_file.name.split('/')[-1]} (Prediction: {obj.prediction})"