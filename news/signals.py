from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Post
from .tasks import send_post_notification


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

        send_post_notification.delay(instance.pk)