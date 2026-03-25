from django.contrib.auth import login as django_login
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from .forms import SignupForm, LoginForm
from .models import User
from utils.email import send_verification_email


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        send_verification_email(self.request, user)
        return render(self.request, 'registration/signup_done.html')


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('cbv_todo_list')

    def form_valid(self, form):
        django_login(self.request, form.get_user())
        return super().form_valid(form)


def verify_email(request):
    code = request.GET.get('code')
    try:
        signer = TimestampSigner()
        email = signer.unsign(code, max_age=60 * 5)
        user = get_object_or_404(User, email=email)
        user.is_active = True
        user.save()
        return render(request, 'registration/verify_success.html')
    except (SignatureExpired, BadSignature):
        return render(request, 'registration/verify_failed.html')