from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post, Category


@shared_task
def send_post_notification(post_id):
    post = Post.objects.get(pk=post_id)
    categories = post.categories.all()

    for category in categories:
        subscribers = category.subscribers.all()
        for user in subscribers:
            html_content = render_to_string('email_news.html', {
                'post': post,
                'username': user.username,
            })

            msg = EmailMultiAlternatives(
                subject=f'Новая статья в категории {category.name}: {post.title}',
                body=f'Здравствуй, {user.username}. Новая статья в категории {category.name}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@shared_task
def send_weekly_newsletter():
    """
    Еженедельная рассылка новых статей за неделю.
    Вызывается по расписанию (понедельник, 8:00).
    """
    from datetime import timedelta
    from django.utils import timezone

    week_ago = timezone.now() - timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=week_ago)

    if not posts.exists():
        return

    for category in Category.objects.all():
        subscribers = category.subscribers.all()
        if not subscribers.exists():
            continue

        category_posts = posts.filter(categories=category)
        if not category_posts.exists():
            continue

        for user in subscribers:
            html_content = render_to_string('email_weekly.html', {
                'posts': category_posts,
                'username': user.username,
                'category': category,
            })

            msg = EmailMultiAlternatives(
                subject=f'Еженедельная рассылка новостей: {category.name}',
                body=f'Здравствуй, {user.username}. Новые статьи за неделю в категории {category.name}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()