from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import re

KEYWORDS = [
    'python', 'django', 'sql', 'machine learning', 'html', 'css', 
    'javascript', 'react', 'node', 'api', 'aws', 'docker', 'java', 'c++', 'git'
]

@login_required
def check_resume(request):
    score = 0
    feedback = []
    matched_keywords = []
    missing_keywords = []

    if request.method == 'POST':
        resume_text = request.POST.get('resume_text', '').lower()
        
        for kw in KEYWORDS:
            # Add simple word boundary regex mapping
            if re.search(r'\b' + re.escape(kw) + r'\b', resume_text):
                matched_keywords.append(kw)
            else:
                missing_keywords.append(kw)
        
        if len(KEYWORDS) > 0:
            score = int((len(matched_keywords) / len(KEYWORDS)) * 100)
        
        if score < 50:
            feedback.append("Consider adding more modern tech keywords to pass ATS systems.")
        if 'python' not in matched_keywords and 'java' not in matched_keywords and 'c++' not in matched_keywords:
            feedback.append("It looks like you are missing core programming languages. Add Python, Java, or C++.")
        if 'git' not in matched_keywords:
            feedback.append("Version control is essential. Add 'Git' to your skills.")

    return render(request, 'resume_checker/check.html', {
        'score': score,
        'feedback': feedback,
        'matched': matched_keywords,
        'missing': missing_keywords[:5],  # suggest at most 5 missing keywords
        'is_post': request.method == 'POST'
    })
