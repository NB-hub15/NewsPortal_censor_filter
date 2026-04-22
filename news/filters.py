import django_filters
from django.forms import DateInput
from .models import Post


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название содержит'
    )

    author = django_filters.CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Имя автора содержит'
    )

    time_in = django_filters.DateFilter(
        field_name='time_in',
        lookup_expr='gt',
        label='Опубликовано после',
        widget=DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['title', 'author', 'time_in']