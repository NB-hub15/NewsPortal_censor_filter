from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'categories']

    def clean(self):
        cleaned_data = super().clean()
        author = cleaned_data.get('author')

        # Проверка: не более 3 новостей за 24 часа (урок 4, стр.6 п.2)
        if author:
            last_24h = timezone.now() - timezone.timedelta(hours=24)
            posts_count = Post.objects.filter(
                author=author,
                time_in__gte=last_24h,
                post_type='NW'
            ).count()

            if posts_count >= 3:
                raise ValidationError(
                    'Нельзя публиковать более 3 новостей в сутки.'
                )

        return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user

