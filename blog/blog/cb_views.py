from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog


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


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'
    # model,template만 가져오면 자동으로 pk를 가져온다, urls에서 pk가 아닌 다른걸 넣으면 사용 할 수 없다.

    # def queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(id__lte=50)

    # def get_object(self, queryset=None) :
    #     object = super(). get_object()
    #     object = self.model.objects.get(pk=self.kwargs.get('pk'))
    #     return object

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['test'] = 'CBV'
    #     return context

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