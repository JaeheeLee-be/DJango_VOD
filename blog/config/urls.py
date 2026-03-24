"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, include
from django.views import View
from django.views.generic import TemplateView, RedirectView

from member import views as member_views


class AboutView(TemplateView):
    template_name = 'about.html'


class TestView(View):
    def get(self, request):
        return render(request, 'test_get.html')

    def post(self, request):
        return render(request, 'test_post.html')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('blog.urls', namespace='blog')),
    path('fb/', include('blog.fbv_urls')),

    # auth
    path('accounts/', include("django.contrib.auth.urls")),
    path('signup/',member_views.sign_up, name='signup'),
    path('login/',member_views.login, name='login'),

    # path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('about/', AboutView.as_view(), name='about'),
    path('redirect/', RedirectView.as_view(pattern_name='about2'), name='redirect'),
    # path('redirect2/', lambda req: redirect('about')), # 익명함수, 다른 방법: lambda req: redirect(reverse('about'))),
    path('test/', TestView.as_view(), name='test'),

    # summernote
    path('summernote/', include('django_summernote.urls')),
]

# media는 static처럼 default 값으로 설정되어 있지 않아, 연결해주기 위해서 작성해줘야 한다
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)