from django.contrib.auth import get_user_model
from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from member.forms import SignUpForm

User = get_user_model()

class SignUpView(FormView):
    template_name = 'auth/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('signup_done')

    def form_valid(self, form):
        user = form.save()
        # 이메일 발송
        signer = TimestampSigner()
        signed_user_email = signer.sign(user.email)
        signer_dump = signing.dumps(signed_user_email)

        # decoded_user_email = signing.loads(signer_dump)
        # email = signer.unsign(decoded_user_email, max_age=60 * 30)

        url = f'{self.request.scheme}://{self.request.META["HTTP_HOST"]}/verify/?code={signer_dump}'

        return render(
            self.request,
            template_name='auth/signup_done.html',
            context={'user': user}
        )


def verify(request):
    code = request.GET.get('code', '')
    # None ==> ''

    signer = TimestampSigner()
    try:
        decoded_user_email = signing.loads(code)
        email = signer.unsign(decoded_user_email, max_age=60 * 30)
    except (TypeError, SignatureExpired):
        return render(request, 'auth/not_verifyed.html')

    user = get_object_or_404(User, email=email, is_active=False)
    user.is_active = True
    user.save()
    # return redirect(reverse('login'))
    return render(request, 'auth/email_not_verifyed.html', {'user': user})