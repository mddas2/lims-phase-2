from rest_framework import serializers
from django.utils.http import urlsafe_base64_decode
from account.models import CustomUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    class Meta:
        fields = ['email',]
        
        
class CustomPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=3)
    
    class Meta:
        fields = ['password',]
        
    def validate(self, data):
        password = data.get("password")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")
        
        if token is None or encoded_pk is None:
            raise serializers.ValidationError("missing data")
        
        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = CustomUser.objects.get(pk=pk)
        
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")
        
        user.set_password(password)
        user.save()
        return data
    
class CustomEmailVerifySerializer(serializers.Serializer):     
    encoded_pk = serializers.CharField()   
    token = serializers.CharField()   

    def validate(self, data):
        token = data.get("token")
        encoded_pk = data.get("encoded_pk")
        # print(token,encoded_pk)
        if token is None or encoded_pk is None:
            raise serializers.ValidationError("missing data")
        
        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = CustomUser.objects.get(pk=pk)
        
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The email verify token is invalid")
        
        user.is_email_verified = True
        user.save()
        return data