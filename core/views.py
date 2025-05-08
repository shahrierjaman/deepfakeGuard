from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, JsonResponse
from .models import Case, Notification, User, AnalysisResult, MediaReport
from .forms import FlagContentForm, UploadMediaForm, MediaReportForm
from .deepfake_model import predict_deepfake
import json

def index(request):
    test_user = User.objects.first()
    user_cases = Case.objects.filter(flagged_by=test_user)
    user_notifications = Notification.objects.filter(user=test_user).order_by('-created_at')[:5]

    # Dynamic data from AnalysisResult
    latest_results = AnalysisResult.objects.order_by('-id')[:2]  # Last 2 analyses
    total_analyzed = AnalysisResult.objects.count()
    deepfake_count = AnalysisResult.objects.filter(prediction__iregex=r'(deepfake|fake)').count()
    authentic_count = total_analyzed - deepfake_count
    flagged_count = 3  # Placeholder; link to MediaReport or Case if available

    # Calculate detection accuracy (simplified; adjust based on your model)
    accuracy = 85.0 if total_analyzed > 0 else 0.0  # Placeholder; use actual model accuracy if available

    # Precompute percentages for the template
    total_analyzed_percentage = total_analyzed / 100 if total_analyzed > 0 else 0
    flagged_percentage = (flagged_count / total_analyzed * 100) if total_analyzed > 0 else 0

    context = {
        'cases': user_cases,
        'notifications': user_notifications,
        'latest_results': latest_results,
        'total_analyzed': total_analyzed,
        'deepfake_count': deepfake_count,
        'authentic_count': authentic_count,
        'flagged_count': flagged_count,
        'accuracy': accuracy,
        'total_analyzed_percentage': total_analyzed_percentage,
        'flagged_percentage': flagged_percentage,
    }
    return render(request, 'index.html', context)

def upload_media(request):
    print(f"[DEBUG] Request method: {request.method}")
    if request.method == 'POST':
        print(f"[DEBUG] Form received: {request.POST}, Files: {request.FILES}")
        form = UploadMediaForm(request.POST, request.FILES)
        if form.is_valid():
            media_type = form.cleaned_data['media_type']
            media_file = form.cleaned_data['media_file']
            print(f"[DEBUG] Form valid: media_type={media_type}, media_file={media_file}")
            try:
                analysis_result = AnalysisResult(
                    media_type=media_type,
                    media_file=media_file,
                    prediction='Pending',
                    confidence=0.0
                )
                analysis_result.save()
                print(f"[DEBUG] Saved AnalysisResult: {analysis_result}, ID: {analysis_result.id}")
                file_path = analysis_result.media_file.path
                print(f"[DEBUG] File path: {file_path}")
                prediction, confidence = predict_deepfake(file_path, media_type)
                analysis_result.prediction = prediction
                analysis_result.confidence = confidence
                analysis_result.save()
                print(f"[DEBUG] Updated AnalysisResult with prediction: {prediction}, confidence: {confidence}")
                return render(request, 'upload-media.html', {
                    'form': UploadMediaForm(),
                    'prediction': prediction,
                    'confidence': round(confidence, 2),
                    'media_type': media_type,
                    'media_url': analysis_result.media_file.url
                })
            except Exception as e:
                print(f"[ERROR] Upload failed: {str(e)}")
                return render(request, 'upload-media.html', {
                    'form': form,
                    'error': f"An error occurred during analysis: {str(e)}"
                })
        else:
            print(f"[ERROR] Form invalid: {form.errors}")
            return render(request, 'upload-media.html', {
                'form': form,
                'error': 'Form validation failed. Please correct the errors and try again.'
            })
    else:
        print("[DEBUG] Rendering upload form")
    return render(request, 'upload-media.html', {'form': UploadMediaForm()})

def flag_content(request):
    print(f"[DEBUG] Flag content request method: {request.method}")
    if request.method == 'POST':
        print(f"[DEBUG] Form data: {request.POST}")
        if not request.POST.get('csrfmiddlewaretoken'):
            print("[ERROR] CSRF token missing")
            return HttpResponseForbidden("CSRF token missing or invalid")
        form = MediaReportForm(request.POST)
        if form.is_valid():
            print(f"[DEBUG] Form valid, saving: {form.cleaned_data}")
            media_report = form.save()
            print(f"[DEBUG] Saved MediaReport: {media_report}, ID: {media_report.id}")
            return render(request, 'flag-content.html', {
                'form': MediaReportForm(),
                'success': True
            })
        else:
            print(f"[ERROR] Form invalid: {form.errors}")
            return render(request, 'flag-content.html', {
                'form': form,
                'error': 'Please correct the errors in the form.'
            })
    else:
        print("[DEBUG] Rendering flag content form")
        form = MediaReportForm()
    return render(request, 'flag-content.html', {'form': form})

def delete_analysis_result(request, result_id):
    if request.method == 'POST':
        try:
            result = AnalysisResult.objects.get(id=result_id)
            result.delete()
            return JsonResponse({'success': True})
        except AnalysisResult.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Result not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def analysis_history(request):
    # Fetch all AnalysisResult entries, ordered by id (descending)
    results = AnalysisResult.objects.all().order_by('-id')

    # Prepare chart data (total counts)
    deepfake_count = results.filter(prediction__iregex=r'(deepfake|fake)').count()
    authentic_count = results.exclude(prediction__iregex=r'(deepfake|fake)').count()
    print(f"[DEBUG] Deepfake count: {deepfake_count}, Authentic count: {authentic_count}")

    chart_data = {
        'labels': json.dumps(['All Entries']),
        'deepfake': json.dumps([deepfake_count]),
        'authentic': json.dumps([authentic_count]),
    }

    context = {
        'results': results,
        'chart_data': chart_data,
    }
    return render(request, 'analysis-history.html', context)

def notifications(request):
    return render(request, 'notification.html')

def settings(request):
    return render(request, 'settings.html')

def investigator_dashboard(request):
    return render(request, 'investigator-dashboard.html')

def case_management(request):
    return render(request, 'case-management.html')

def deepfake_analysis(request):
    return render(request, 'deepfake-analysis.html')

def admin_dashboard(request):
    return render(request, 'admin-dashboard.html')

def user_management(request):
    return render(request, 'user-management.html')

def system_analysis(request):
    return render(request, 'system-analysis.html')

def flagged_content(request):
    return render(request, 'flagged-content.html')

"""
def upload_media(request):
    print(f"[DEBUG] Request method: {request.method}")
    if request.method == 'POST':
        print(f"[DEBUG] Form received: {request.POST}, Files: {request.FILES}")
        form = UploadMediaForm(request.POST, request.FILES)
        if form.is_valid():
            media_type = form.cleaned_data['media_type']
            media_file = form.cleaned_data['media_file']
            print(f"[DEBUG] Form valid: media_type={media_type}, media_file={media_file}")
            try:
                analysis_result = AnalysisResult(
                    media_type=media_type,
                    media_file=media_file,
                    prediction='Pending',
                    confidence=0.0
                )
                analysis_result.save()
                print(f"[DEBUG] Saved AnalysisResult: {analysis_result}, ID: {analysis_result.id}")
                file_path = analysis_result.media_file.path
                print(f"[DEBUG] File path: {file_path}")
                prediction, confidence = predict_deepfake(file_path, media_type)
                analysis_result.prediction = prediction
                analysis_result.confidence = confidence
                analysis_result.save()
                print(f"[DEBUG] Updated AnalysisResult with prediction: {prediction}, confidence: {confidence}")
                return render(request, 'upload-media.html', {
                    'form': UploadMediaForm(),
                    'prediction': prediction,
                    'confidence': round(confidence, 2),
                    'media_type': media_type,
                    'media_url': analysis_result.media_file.url
                })
            except Exception as e:
                print(f"[ERROR] Upload failed: {str(e)}")
                return render(request, 'upload-media.html', {
                    'form': form,
                    'error': f"An error occurred during analysis: {str(e)}"
                })
        else:
            print(f"[ERROR] Form invalid: {form.errors}")
            return render(request, 'upload-media.html', {
                'form': form,
                'error': 'Form validation failed. Please correct the errors and try again.'
            })
    else:
        print("[DEBUG] Rendering upload form")
    return render(request, 'upload-media.html', {'form': UploadMediaForm()})
"""