from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
import csv
from .models import Question, TestResult
from .forms import QuestionCSVUploadForm


def is_admin(user):
    return user.is_superuser or user.is_staff


# =========================
# TAKE TEST VIEW (FIXED)
# =========================
@login_required
def take_test(request):
    questions = Question.objects.all().order_by('?')[:10]

    if request.method == 'POST':
        score = 0
        total = questions.count()

        for q in questions:
            selected_answer = request.POST.get(f'question_{q.id}')
            if selected_answer == q.correct_option:
                score += 1

        percentage = round((score / total) * 100, 1) if total > 0 else 0

        TestResult.objects.create(
            user=request.user,
            score=score,
            total=total,
            percentage=percentage,
            test_name="General Technical Screen"
        )

        return redirect('test_result')

    return render(request, 'mocktest/take_test.html', {
        'questions': questions
    })


# =========================
# RESULT VIEW (UPDATED)
# =========================
@login_required
def test_result(request):
    results = TestResult.objects.filter(user=request.user).order_by('-date_taken')
    return render(request, 'mocktest/result.html', {
        'results': results
    })


# =========================
# CSV UPLOAD (IMPROVED)
# =========================
@user_passes_test(is_admin)
def upload_questions_csv(request):
    if request.method == 'POST':
        form = QuestionCSVUploadForm(request.POST, request.FILES)

        if form.is_valid():
            csv_file = request.FILES['csv_file']

            if not csv_file.name.endswith('.csv'):
                messages.error(request, "Please upload a valid CSV file.")
                return redirect('upload_questions_csv')

            try:
                decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
                reader = csv.DictReader(decoded_file)

                required_columns = [
                    'question', 'option1', 'option2',
                    'option3', 'option4', 'answer'
                ]

                if not reader.fieldnames or not all(col in reader.fieldnames for col in required_columns):
                    messages.error(request, "Invalid CSV format. Required columns missing.")
                    return redirect('upload_questions_csv')

                success_count = 0
                error_count = 0
                valid_answers = ['A', 'B', 'C', 'D']

                for row_num, row in enumerate(reader, start=2):
                    try:
                        answer = row['answer'].strip().upper()

                        if answer not in valid_answers:
                            raise ValueError("Invalid answer option")

                        Question.objects.create(
                            text=row['question'].strip(),
                            option_a=row['option1'].strip(),
                            option_b=row['option2'].strip(),
                            option_c=row['option3'].strip(),
                            option_d=row['option4'].strip(),
                            correct_option=answer
                        )

                        success_count += 1

                    except Exception:
                        error_count += 1

                if error_count == 0:
                    messages.success(request, f"{success_count} questions uploaded successfully.")
                else:
                    messages.warning(
                        request,
                        f"{success_count} uploaded, {error_count} rows skipped due to errors."
                    )

                return redirect('admin_dashboard')

            except Exception as e:
                messages.error(request, f"Error processing file: {str(e)}")
                return redirect('upload_questions_csv')

    else:
        form = QuestionCSVUploadForm()

    return render(request, 'mocktest/upload_csv.html', {
        'form': form,
        'title': 'Upload Questions via CSV'
    })


# =========================
# DOWNLOAD SAMPLE CSV
# =========================
@user_passes_test(is_admin)
def download_sample_questions_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_questions.csv"'

    writer = csv.writer(response)
    writer.writerow(['question', 'option1', 'option2', 'option3', 'option4', 'answer'])

    writer.writerow([
        'What is the time complexity of binary search?',
        'O(1)', 'O(n)', 'O(log n)', 'O(n^2)', 'C'
    ])

    writer.writerow([
        'Which data structure uses LIFO?',
        'Queue', 'Stack', 'Tree', 'Graph', 'B'
    ])

    return response