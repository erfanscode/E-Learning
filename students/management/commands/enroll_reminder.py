import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone


class Command(BaseCommand):
    help = 'Send reminder emails to \
      students who have not enrolled in a course'
    
    def add_arguments(self, parser):
        parser.add_argument('--days', dest='days', type=int)

    def handle(self, *args, **options):
        emails = []
        subject = 'Enroll in a course'
        date_joined = timezone.now().today() - \
            datetime.timedelta(days=options['days'] or 0)
        users = User.objects.annotate(course_count=Count('courses_joined')).filter(course_count=0, date_joined__lte=date_joined)
        for user in users:
            message = """ عزیز متوجه شدیم که در هیچ دوره‌ای ثبت نام نکرده‌اید، منتظر چی هستید؟ {} """.format(user.first_name)
            emails.append((subject,
                           message,
                           settings.DEFAULT_FROM_EMAIL,
                           [user.email]))
        send_mass_mail(emails)
        self.stdout.write('یادآوری {} ارسال شد.'.format(len(emails)))
