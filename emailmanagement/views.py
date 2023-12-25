from django.shortcuts import render
from rest_framework import generics, status, viewsets, response
from .serializers import EmailSerializer, CustomPasswordResetSerializer,CustomEmailVerifySerializer
from account.models import CustomUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

site_f  = "https://lims.dftqc.gov.np" #http://localhost:4200"#"https://dev-lims.netlify.app"#"https://lims.dftqc.gov.np"

class EmailCheckView(generics.GenericAPIView):
    serializer_class = EmailSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = CustomUser.objects.filter(email=email).first()
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            
            reset_url = f"{site_f}/password-reset?pk={encoded_pk}&token={token}"
            email = user.email
            subject = 'Password Reset Link'
            reset_verification = "reset_password"
            sendMail(email, reset_url,subject,reset_verification)
            
            return response.Response(
                {
                "message": "password reset link has been sent to your email address"
                },
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                {"message": "User doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CustomPasswordResetView(generics.GenericAPIView):
    serializer_class = CustomPasswordResetSerializer
    
    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"kwargs":kwargs})
        serializer.is_valid(raise_exception=True)
        
        return response.Response(
            {"message": "Password Reset Complete"},
            status=status.HTTP_200_OK,
        )

class EmailVerificationConfirmView(APIView):
    serializer_class = CustomEmailVerifySerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"kwargs":kwargs})
        serializer.is_valid(raise_exception=True)
        
        return response.Response(
            {"message": "Email Verified Complete",'verified':True},
            status=status.HTTP_200_OK,
        )

class SendEmailVerificationLink(APIView):
    
    def post(self, request, *args, **kwargs):
        import uuid
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email).first()

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({
                'detail': 'User with this email does not exist.',
            }, status=status.HTTP_400_BAD_REQUEST)

        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        # Send the token via email
        subject = 'Email Verification Token'
        verify_url = f"{site_f}/user-verification-success?pk={encoded_pk}&token={token}"
        subject = 'Email Verification Link '
        reset_verification = "verification"
        sendMail(email,verify_url,subject,reset_verification)

        return Response({
            'detail': 'Email verificatio'})

def sendMail(email, reset_url,subject,reset_verification):
    if reset_verification == "verification":
        body = f"""<body>
            <table align="center" cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width: 600px; font-family: Poppins; background: whitesmoke; padding: 20px; border-radius: 6px;">
                <tr>
                    <td align="center" bgcolor="#FFFFFF" style="padding: 20px;">
                        <img src="http://lims.dftqc.gov.np/assets/nepal-government.png" alt="" width="132" style="display: block; margin: 0 auto;">
                        <p style="color: #0B53A7; font-weight: 600; font-size: 18px; margin-top: 20px;">Labrotary Information Management System (LIMS)</p>
                        <p style="color: #0B53A7; font-weight: 600; font-size: 18px; margin-top: 20px;">Please verify your account</p>
                        <p style="text-align: center; font-weight: 400;">Click the button below to verify your account.</p>
                        <a href="{reset_url}" style="text-decoration: none; background: #0B53A7; color: #FFFFFF; padding: 10px 20px; border-radius: 3px; display: inline-block; margin-top: 15px;">Verify Your Account</a>
                        <p style="text-align: center; margin-top: 20px;">Please visit <a href="http://lims.dftqc.gov.np" style="text-decoration: none; color: #0B53A7; font-weight: 600;">www.lims.dftqc.gov.np</a> for any enquiries.</p>
                        <p style="margin: 0; text-align: center;"><span style="font-weight: 600;">Tel:</span> 977-1-4262369, 4262430, 4240016, 4262739</p>
                        <p style="margin: 0; text-align: center; text-decoration: none;"><span style="font-weight: 600;">Fax:</span> 977-1-4262337 <span style="font-weight: 600; margin-left: 10px;">E-mail:</span> info@dftqc.gov.np</p>
                    </td>
                </tr>
            </table>
        </body>
        </html>"""
    else:
        body = f"""<body>
            <table align="center" cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width: 600px; font-family: Poppins; background: whitesmoke; padding: 20px; border-radius: 6px;">
                <tr>
                    <td align="center" bgcolor="#FFFFFF" style="padding: 20px;">
                        <img src="http://lims.dftqc.gov.np/assets/nepal-government.png" alt="" width="132" style="display: block; margin: 0 auto;">
                        <p style="color: #0B53A7; font-weight: 600; font-size: 18px; margin-top: 20px;">Labrotary Information Management System (LIMS)</p>
                        <p style="color: #0B53A7; font-weight: 600; font-size: 18px; margin-top: 20px;">Please change your Password</p>
                        <p style="text-align: center; font-weight: 400;">Click the button below to change the password of your account.</p>
                        <a href="{reset_url}" style="text-decoration: none; background: #0B53A7; color: #FFFFFF; padding: 10px 20px; border-radius: 3px; display: inline-block; margin-top: 15px;">Change Password</a>
                        <p style="text-align: center; margin-top: 20px;">Please visit <a href="http://lims.dftqc.gov.np" style="text-decoration: none; color: #0B53A7; font-weight: 600;">www.lims.dftqc.gov.np</a> for any enquiries.</p>
                        <p style="margin: 0; text-align: center;"><span style="font-weight: 600;">Tel:</span> 977-1-4262369, 4262430, 4240016, 4262739</p>
                        <p style="margin: 0; text-align: center; text-decoration: none;"><span style="font-weight: 600;">Fax:</span> 977-1-4262337 <span style="font-weight: 600; margin-left: 10px;">E-mail:</span> info@dftqc.gov.np</p>
                    </td>
                </tr>
            </table>
        </body>
        </html>"""
    html_contents = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Template</title>
            <style>
                @import url("https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap");
            </style>
        </head>""" + body
    
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    plain_message = ""
    send_mail(subject, plain_message, email_from, recipient_list,html_message=html_contents)
    