from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.urls import reverse


def send_verification_email(request, user):
    signer = TimestampSigner()
    signed_value = signer.sign(user.email)

    verify_url = request.build_absolute_uri(
        reverse('verify') + f'?code={signed_value}'
    )

    send_mail(
        subject='이메일 인증을 완료해주세요',
        message=f'아래 링크를 클릭하여 이메일 인증을 완료해주세요.\n\n{verify_url}',
        from_email=None,  # settings.py의 EMAIL_HOST_USER 사용
        recipient_list=[user.email],
    )