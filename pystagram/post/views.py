from django.shortcuts import render
from django.views.generic import ListView

from post.models import Post


class PostListView(ListView):
    queryset = Post.objects.all().select_related('user').prefetch_related('images')
    # select_related: Post가 FK를 가지고 있으면 가능, 개발적으로는 sql에서 join해서 가져옴
    # prefetch_related: 역참조, PostImage가 FK로 Post를 가지고 있을 때, ManyToMany(N:N) 일 때 사용,
                        # 연관되어 있는 것들 python에서 알아서 가져옴, sql에서 한 번 더 요청
    template_name = 'post/list.html'
    paginate_by = 20
    ordering = ('-created_at', )