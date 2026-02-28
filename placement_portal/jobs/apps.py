from django.apps import AppConfig

class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs'

    def ready(self):
        try:
            import jobs.scheduler
            jobs.scheduler.start_reminder_thread()
        except:
            pass
