HIRELY career Placement Assistance Portal

Hirely is a full-stack Django web application designed to streamline student placement preparation. It centralizes resume analysis, job tracking, and interview practice into one structured platform built with Django and styled using Tailwind CSS.

# Project description

Hirely solves a common student problem — placement preparation tools are scattered across multiple platforms.
This system provides a centralized portal where students can:

Analyze resumes using ATS logic

Take mock interview tests

View job opportunities filtered by qualification

Receive structured placement guidance

The application includes role-based routing for Admins and Students.

# Tech stack

Python 3.8+

Django

Django AllAuth (Authentication)

Tailwind CSS

SQLite (Default Database)

HTML5

CSS3

# core features 

 Authentication System

Secure login (username/email)

Password reset (console-based backend)

Role-based routing (Admin / Student)

 ATS Resume Checker

PDF parsing

Stopword removal using NLTK

Keyword matching

Resume scoring logic

 Mock Interview System

Randomized question selection

10-question automatic test generation

Auto evaluation & scoring

 Job Portal

Qualification-based job filtering

Admin bulk CSV upload

Structured job listings

 Admin Dashboard

Job CSV bulk upload

Mock Question CSV bulk upload

Controlled admin panel access
# installation commands 
cd placement_portal
 Create Virtual Environment

python -m venv venv
venv\Scripts\activate

 Install Dependencies
pip install -r requirements.txt

 Database Setup
python manage.py makemigrations
python manage.py migrate

 Create Superuser (Admin Access)
python manage.py createsuperuser

Follow prompts to set username, email, and password.

 Required NLTK Setup (Resume Checker)

Open Python shell:

python

Then run:

import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
exit()

This is mandatory before first run.

# run the application
python manage.py runserver

Open browser:

http://127.0.0.1:8000/

# screenshots

![Login Page](C:\Users\User\Pictures\Screenshots\Screenshot 2026-02-28 100413.png)
![Home Page](C:\Users\User\Pictures\Screenshots\Screenshot 2026-02-28 100434.png)
![Mock Test](C:\Users\User\Pictures\Screenshots\Screenshot 2026-02-28 100500.png)
![Result](C:\Users\User\Pictures\Screenshots\Screenshot 2026-02-28 100552.png)

# TEAM MEMBERS 

ASNA O S 
JOSIYA ANTONY
(Project Designed & Developed)

# Licence

This project is licensed under the MIT License.

## . Running the Application
Spin up the local development server:
cmd
python manage.py runserver


Open a web browser and navigate directly to: http://127.0.0.1:8000/

---

## Technical Project Features Checklist

### Authentication (Django AllAuth)
- The login loop utilizes username/email dual-authorization seamlessly.
- *Forgot Password*: Fully fleshed out routing via the console. If you click "Forgot Password", look directly into your terminal/CMD running the server to catch the specific encoded link logic (as EMAIL_BACKEND is set to console). 
- To shift password resets onto production Gmail/SMTP in the future, remove django.core.mail.backends.console.EmailBackend from your settings.py and replace it with proper EMAIL_HOST credentials.

### Admin Dashboard Tooling (Superusers only)
- Admin accounts have unique access paths routing them to /accounts/admin-panel/.
- CSV Bulk Uploader for Jobs requires: title, company, qualification, description, interview_date, application_link. Dates must strictly format as YYYY-MM-DD.
- CSV Bulk Uploader for Questions requires: question, option1, option2, option3, option4, answer. Answers must exactly match the character A, B, C, or D. 

### Target Student Flow (Standard Users)
- General users route instantly to /accounts/dashboard/.
- Jobs: Renders Target matches exclusively built from their profile's Custom 'Qualification' field!
- Mock Test: Auto-pulls randomized sets of 10 live questions explicitly pulled from the Mock Questions database uploaded by the Admin.
