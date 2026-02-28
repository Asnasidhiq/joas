# HIRELY CAREER SETUP GUIDE

Welcome to the Hirely career , a comprehensive web application for managing student placements,resumes , interview preparationsbuilt cleanly with django and sthyles beautifully with tailwind css.

This guide covers everything you need to start the project.

## Prerequisites
Before you begin, ensure you have the following installed on your system:
- *Python 3.8+*: Ensure python is added to your environment paths.
- *Pip*: The Python package manager.

## 1. Local Environment Setup

Clone or place the project folder on your machine, then navigate inside the placement_portal directory where manage.py lives.

### Create a Virtual Environment (Recommended)
It is highly recommended to isolate the project dependencies.
cmd
python -m venv venv
venv\Scripts\activate



### Install Dependencies
Run the following command to securely fetch and install all required modules exactly mapped in our setup list:
cmd
pip install -r requirements.txt

Note: Key libraries installed include django, django-allauth, PyPDF2, nltk, and custom machine learning packages for resume checking.

## 2. Database Creation & Syncing
Django provides an easy built-in SQLite database by default. Execute these to sync all tables:

cmd
python manage.py makemigrations
python manage.py migrate


## 3. Creating the Superuser (Admin Access)
To access the Admin Dashboard (needed for adding jobs via CSV, mock questions, etc.), you must create a standard superuser.

cmd
python manage.py createsuperuser

Follow the prompts to configure an Administrator Username, Email, and Password. 

## 4. Required Data Packages for Resume Checker
The ATS Resume checker utilizes nltk (Natural Language Toolkit) behind the scenes to verify stopwords and compute matching algorithms. *You must download these exact datasets into python once before your first run:*

Open your python shell via terminal:
cmd
python

Execute these lines exactly:
python
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
exit()


## 5. Running the Application
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
