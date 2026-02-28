from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
import csv
from .models import Job
from .forms import JobCSVUploadForm

def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
def job_list(request):
    # Filter jobs based on student's qualification safely
    user_qual = getattr(request.user.profile, 'qualification', '') if hasattr(request.user, 'profile') else ''
    
    if user_qual:
        # Simple case insensitive contains match
        jobs = Job.objects.filter(required_qualification__icontains=user_qual).order_by('interview_date')
    else:
        jobs = Job.objects.all().order_by('interview_date')
        
    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'user_qual': user_qual})

@user_passes_test(is_admin)
def upload_jobs_csv(request):
    if request.method == 'POST':
        form = JobCSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            try:
                decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
                reader = csv.DictReader(decoded_file)
                
                required_columns = ['title', 'company', 'qualification', 'description', 'interview_date', 'application_link']
                
                if not reader.fieldnames or not all(col in reader.fieldnames for col in required_columns):
                    messages.error(request, "Invalid CSV format. Please ensure all required columns are present.")
                    return redirect('upload_jobs_csv')
                
                success_count = 0
                error_count = 0
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # parse date
                        interview_date = datetime.strptime(row['interview_date'].strip(), '%Y-%m-%d')
                        Job.objects.create(
                            title=row['title'].strip(),
                            company=row['company'].strip(),
                            required_qualification=row['qualification'].strip(),
                            description=row['description'].strip(),
                            interview_date=interview_date,
                            application_link=row.get('application_link', '').strip()
                        )
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        
                if error_count == 0:
                    messages.success(request, f"Successfully uploaded {success_count} jobs.")
                else:
                    messages.warning(request, f"Uploaded {success_count} jobs, but {error_count} rows had errors (e.g., bad date format).")
                return redirect('admin_dashboard')
            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
                return redirect('upload_jobs_csv')
    else:
        form = JobCSVUploadForm()
        
    return render(request, 'jobs/upload_csv.html', {'form': form, 'title': 'Upload Jobs via CSV'})

@user_passes_test(is_admin)
def download_sample_jobs_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_jobs.csv"'
    writer = csv.writer(response)
    writer.writerow(['title', 'company', 'qualification', 'description', 'interview_date', 'application_link'])
    writer.writerow(['Software Engineer', 'Company Inc', 'B.Tech CS', 'We are looking for a strong dev.', '2026-05-15', 'https://example.com/apply'])
    return response
