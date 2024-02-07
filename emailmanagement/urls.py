from django.urls import path
from .views import EmailCheckView, CustomPasswordResetView , EmailVerificationConfirmView , SendEmailVerificationLink



urlpatterns = [
    path('password-reset/', EmailCheckView.as_view()),
    path('password-reset/<str:encoded_pk>/<str:token>/', CustomPasswordResetView.as_view(), name="reset-password"),

    path('verify-email-confirm/', EmailVerificationConfirmView.as_view(), name='verify-email-confirm'),
    path('send-verification-to-email/', SendEmailVerificationLink.as_view(), name='send-veri'),
]
