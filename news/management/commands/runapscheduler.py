import logging

from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from news.models import Post, Category

logger = logging.getLogger(__name__)



def weekly_newsletter():
    today = timezone.now()
    last_week = today - timezone.timedelta(days=7)

    for category in Category.objects.all():
        new_posts = Post.objects.filter(
            categories=category,
            time_in__gte=last_week
        )

        if not new_posts.exists():
            continue

        for subscriber in category.subscribers.all():
            html_content = render_to_string(
                'email_weekly.html',
                {
                    'username': subscriber.username,
                    'category': category,
                    'posts': new_posts,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'Еженедельная рассылка: {category.name}',
                body='',
                from_email=None,
                to=[subscriber.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            logger.info(f'Письмо отправлено {subscriber.email}')


def delete_old_job_executions(max_age=604_800):

    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")


        scheduler.add_job(
            weekly_newsletter,
            trigger=CronTrigger(
                day_of_week="mon",
                hour="08",
                minute="00",
            ),
            id="weekly_newsletter",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_newsletter'.")


        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon",
                hour="00",
                minute="00",
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")