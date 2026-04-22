from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from .models import Post
from .filters import PostFilter
from .forms import PostForm


class NewsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(post_type='NW').order_by('-time_in')


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'


class NewsSearch(FilterView):
    model = Post
    template_name = 'news_search.html'
    filterset_class = PostFilter
    context_object_name = 'news'
    paginate_by = 10


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_form.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        return super().form_valid(form)


class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_form.html'


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('news_list')