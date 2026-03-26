from django.conf import settings
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.urls import reverse


def send_verification_email(request, user):
    signer = TimestampSigner()
    signed_value = signer.sign(user.email)

    verify_url = request.build_absolute_uri(
        reverse('verify') + f'?code={signed_value}'
    )

    if settings.DEBUG:
        print(f'인증 URL: {verify_url}')
    else:
        send_mail(
            subject='이메일 인증을 완료해주세요',
            message=f'아래 링크를 클릭하여 이메일 인증을 완료해주세요.\n\n{verify_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )