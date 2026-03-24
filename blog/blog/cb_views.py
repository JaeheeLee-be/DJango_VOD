# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog, Comment
from blog.forms import CommentForm


class BlogListView(ListView):
    # model = Blog, 자동으로 objects.all()을 가져옴 (오름차순)
    queryset = Blog.objects.all().order_by('-created_at') # 내림차순 (어디서든 사용가능),
    # ordering = ('-created_at' ,) CBV의 ListView 등에서 클래스 속성으로 사용
    template_name = 'blog_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q)
            )
        return queryset


class BlogDetailView(ListView):
    model = Comment
    queryset = Blog.objects.all().prefetch_related('comment_set', 'comment_set__author')
    # 미리 관련 데이터를 한꺼번에 가져와서 DB조회를 하기 때문에 DB 요청횟수를 줄일 수 있다.
    template_name = 'blog_detail.html'
    # model,template만 가져오면 자동으로 pk를 가져온다, urls에서 pk가 아닌 다른걸 넣으면 사용 할 수 없다.
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Blog, pk=kwargs['blog_pk'])
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(blog=self.object).prefetch_related('author')

    # def queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(id__lte=50)

    # def get_object(self, queryset=None) :
    #     object = super(). get_object()
    #     object = self.model.objects.get(pk=self.kwargs.get('pk'))
    #     return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['blog'] = self.object
        return context

    # def post(self, *args, **kwargs):
    #     comment_form = CommentForm(self.request.POST)
    #
    #     if not comment_form.is_valid():
    #         self.object = self.get_object()
    #         context = self.get_context_data(object=self.object)
    #         context['comment_form'] = comment_form
    #         return self.render_to_response(context)
    #
    #     if not self.request.user.is_authenticated:
    #         raise Http404
    #
    #     comment = comment_form.save(commit=False)
    #     # comment.blog_id = self.kwargs['pk']
    #     comment.author = self.request.user
    #     comment.save()
    #
    #     return HttpResponseRedirect(reverse_lazy('blog:detail', kwargs={'pk': self.kwargs['pk']}))


class BlogCreateView(LoginRequiredMixin, CreateView): # LoginRequiredMixin = @login_required() 같은 기능
    model = Blog
    template_name = 'blog_form.html'
    fields = ['category', 'title', 'content']
    # success_url = reverse_lazy('cb_blog_list') 정적인 page로 갈 때는 활용하는게 좋다.


    def form_valid(self, form):
        self.object = form.save(commit=False) # DB를 콜하지 않음
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url()) # (self.get_success_url()): Django에서 권장, 기본값


    # def get_success_url(self):
    #     return reverse_lazy('cb_blog_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '작성'
        context['btn_name'] = '생성'
        return context

        # test_dict = {
        #     'a': 1,
        #     'b': 2,
        #     'c': 3,
        # }

        # self.test(a=test_dict['a'], b=test_dict['b'], c=test_dict['c'])
        # self.test(**test_dict)
        #
        # test_list = [1, 2, 3]
        # self.test(test_list[0], test_list[1], test_list[2])
        # self.test(*test_list)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'blog_form.html'
    fields = ['category', 'title', 'content']


    def get_queryset(self):    # user가 같은 user인지 걸러내는 방법
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user) # 필터가 잘 되고 있는걸 확인할 수 있다.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '수정'
        context['btn_name'] = '수정'
        return context

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #
    #     if self.object.author != self.request.user:
    #         raise Http404
    #     return self.object / get_queryset 과 get_object 중에 하나를 써도 되지만 queryset이 코드가 짧기 때문에 추천


    # def get_success_url(self):
    #     return reverse_lazy('cb_blog_detail', kwargs={'pk': self.object.pk})
    # get_success를 사용해도 되지만 models에 absolute_url(디테일 페이지) 사용하는 방법도 있다.


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('blog:list')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = CommentForm
    form_class = CommentForm

    def get(self, *args, **kwargs):
        raise Http404
        # CreateView는 기본적으로 get요청이 들어가 있기 때문에 get 요청을 막아주기 위해서 404를 넣음

    def form_valid(self, form):
        blog = self.get_blog()
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.blog = blog
        self.object.save()
        return HttpResponseRedirect(reverse('blog:detail', kwargs={'blog_pk': blog.pk}))

    def get_blog(self):
        pk = self.kwargs['blog_pk'] # kwargs['pk']로 하면 comment model이여서 comment의 pk와 헷갈릴 수 있기 때문에 변경
        blog = get_object_or_404(Blog, pk=pk)
        return blog

# /comment/create/<int:blog_pk>/
# 위에 만든 class는 편하지만 get 변경해줘야 하는것과 detail.html에서 form에 action 추가와 urls 추가해야 하는 번거로움이 있다.