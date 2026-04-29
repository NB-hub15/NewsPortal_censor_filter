from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Post


@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':

        today = timezone.now()
        last_24h = today - timezone.timedelta(hours=24)
        posts_today = Post.objects.filter(
            author=instance.author,
            time_in__gte=last_24h,
            post_type='NW'
        ).count()

        if posts_today > 4:
            raise ValidationError(
                'Нельзя публиковать более 3 новостей в сутки.'
            )

        for category in instance.categories.all():
            for subscriber in category.subscribers.all():
                html_content = render_to_string(
                    'email_news.html',
                    {
                        'post': instance,
                        'username': subscriber.username,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=instance.title,
                    body='',
                    from_email=None,
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()