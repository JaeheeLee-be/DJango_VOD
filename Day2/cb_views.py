from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator

from .models import Todo, Comment
from .forms import CommentForm


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todo/todo_list.html'
    paginate_by = 10
    ordering = ('-created_at',)

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)

        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q)|
                Q(description__icontains=q)
            )
        return queryset


class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'todo/todo_info.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self.request.user.is_superuser and obj.user != self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo'] = self.object.__dict__

        comments = self.object.comments.all().prefetch_related('user')
        paginator = Paginator(comments, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['comment_form'] = CommentForm()
        context['page_obj'] = page_obj
        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = 'todo/todo_create.html'
    fields = ['title', 'description', 'start_date', 'end_date']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.pk})


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    template_name = 'todo/todo_update.html'
    fields = ['title', 'description', 'start_date', 'end_date']

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self.request.user.is_superuser and obj.user != self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.pk})


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    template_name = 'todo/todo_info.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self.request.user.is_superuser and obj.user != self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_list')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['message']
    pk_url_kwarg = 'todo_id'
    template_name = 'todo/todo_info.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.todo = Todo.objects.get(pk=self.kwargs['todo_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.kwargs['todo_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todo = Todo.objects.get(pk=self.kwargs['todo_id'])
        context['todo'] = todo.__dict__
        context['comment_form'] = self.get_form()
        context['page_obj'] = todo.comments.all()
        return context

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['message']
    template_name = 'todo/comment_update.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self.request.user.is_superuser and obj.user != self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.todo.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self.request.user.is_superuser and obj.user != self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.todo.pk})