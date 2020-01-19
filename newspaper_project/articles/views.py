from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView,DetailView,DeleteView
from django.views.generic.edit import CreateView,UpdateView
from .models import Article
from django.urls import reverse_lazy

class ArticleListView(LoginRequiredMixin,ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'article_list.html'


class ArticleDetailView(LoginRequiredMixin,DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'article_detail.html'


class ArticleUpdateView(LoginRequiredMixin,UpdateView):
    model = Article
    template_name = 'article_update.html'
    fields = ('title','body')

    def dispatch(self,request,*args,**kwargs):
        obj = self.get_object()

        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)

class ArticleDeleteView(LoginRequiredMixin,DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

    def dispatch(self,request, *args, **kwargs):
        obj = self.get_object()

        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)

class ArticleCreateView(LoginRequiredMixin,CreateView):
    model = Article
    template_name = 'article_create.html'
    fields = ('title','body')

    def form_valid(self,form):
        model  = form.save(commit=False)
        model.author = self.request.user
        model.save()
        # form.instance.authour = self.request.user
        return super().form_valid(form)
