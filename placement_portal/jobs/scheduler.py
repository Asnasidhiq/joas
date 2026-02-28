import threading
import time
from datetime import timedelta
from django.utils import timezone

def start_reminder_thread():
    def reminder_task():
        while True:
            from .models import Job
            import logging
            logger = logging.getLogger(__name__)
            try:
                now = timezone.now()
                # Check for interviews happening in exactly 1-2 days
                upcoming = Job.objects.filter(
                    interview_date__gte=now + timedelta(days=1),
                    interview_date__lte=now + timedelta(days=2)
                )
                for job in upcoming:
                    print(f"[REMINDER] Upcoming Interview: {job.title} at {job.company} on {job.interview_date}")
            except Exception as e:
                pass
            time.sleep(86400) # Sleep for a day
            
    thread = threading.Thread(target=reminder_task, daemon=True)
    thread.start()
