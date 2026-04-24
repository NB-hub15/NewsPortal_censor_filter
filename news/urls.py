from django.urls import path
from .views import (
    NewsList, NewsDetail, NewsSearch,
    NewsCreate, NewsUpdate, NewsDelete
)
from .views import upgrade_me

urlpatterns = [
    path('upgrade/', upgrade_me, name='upgrade'),
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),

    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
]