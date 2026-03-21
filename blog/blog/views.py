from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import Http404
from django.views.decorators.http import require_http_methods

from blog.forms import BlogForm
from blog.models import Blog


def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at') # created 오름차순 앞에 -를 붙이면 내림차순이 된다.

    q = request.GET.get('q')
    if q:
        blogs = blogs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        ) # Django 내장기능으로 OR검색, |대신 &를 사용하면 AND검색

        # blogs = blogs.filter(title__icontains=q) # 제목 , 본문은 (content__icontains=q)

    paginator = Paginator(blogs, 10)
    page = request.GET.get('page')
    page_object = paginator.get_page(page)

    context = {
        'object_list': page_object.object_list,
        'page_obj': page_object,
    }
    return render(request, 'blog_list.html', context)


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {'blog': blog}
    return render(request, 'blog_detail.html', context)


@login_required     # setting에 login url로 보내줌
def blog_create(request):

    # if not request.users.is_authenticated:
    #     return redirect('login')

    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False) # model 생성
        blog.author = request.user     # 현재 로그인 된 유저를 넣음
        blog.save()
        return redirect(reverse('fb:detail', kwargs={'pk': blog.pk}))

    #     form = BlogForm(request.POST)
    #     if form.is_valid():
    #         blog = form.save()
    #         return redirect(reverse('blog_detail', {'pk': blog.pk}))
    # else:
    #     form = BlogForm()

    context = {'form': form}
    return render(request, 'blog_form.html', context)


def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user) # pk와 author와 request.user를 확인
    # if request.users != blog.author:
    #     raise Http404

    form = BlogForm(request.POST or None, instance=blog)
    if form.is_valid():
        blog = form.save()
        return redirect(reverse('fb:detail', kwargs={'pk': blog.pk}))

    context = {
        'form': form,
    }
    return render(request, 'blog_form.html', context)




# 쿠키의 세션에서 사용한 blog_list
# def blog_list_with_cookie and session(request):
#     blogs = Blog.objects.all()
#
#     visits = int(request.COOKIES.get('visits', 0)) + 1
#     # visits: 쿠키에 방문 횟수를 저장하는 변수
#
#     request.session['count'] = request.session.get('count', 0) + 1
#
#     context = {
#         'blogs': blogs,
#         'count': request.session['count']
#     }
#     response = render(request, 'blog_list.html', context)
#
#     response.set_cookie('visits', visits)
#
#     return response

@login_required()
@require_http_methods([['POST']])
def blog_delete(request, pk):
    # if request.method != 'POST':
    #     raise Http404()
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    blog.delete()

    return redirect(reverse('fb:list'))