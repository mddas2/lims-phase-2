from rest_framework import serializers
from management.serializers import ClientCategorySerializer
from django.contrib.auth.models import Group,Permission
from account.models import CustomUser,CustomUserImages
from django.contrib.auth.hashers import make_password
from management import roles

class CustomUserImageSerializer(serializers.ModelSerializer):
     class Meta:
        ref_name = "CustomUserImageSerializer"
        model = CustomUserImages
        fields = '__all__'

class ApprovedBySerializer(serializers.ModelSerializer):
     class Meta:
        ref_name = "ApprovedBySerializer_account"
        model = CustomUser
        fields = ['first_name','last_name','id','email','role','username'] 

class CustomUserReadSerializer(serializers.ModelSerializer):
     custom_user_image = CustomUserImageSerializer(many = True,read_only = True)
     approved_by = ApprovedBySerializer(read_only = True)
     class Meta:
        ref_name =  "account serializers"
        model = CustomUser
        fields = '__all__' 

class CustomUserReadLimitedSerializer(serializers.ModelSerializer):
     class Meta:
        ref_name =  "CustomUserReadLimitedSerializer serializers"
        model = CustomUser
        fields = ['id','email','first_name','username'] 

class userAdminLevelDataSerializer(serializers.ModelSerializer):
     class Meta:
        ref_name =  "CustomUserReadLimitedSerializer2 serializers"
        model = CustomUser
        fields = ['id','email','first_name','username','last_name','position'] 


class CustomUserSerializer(serializers.ModelSerializer):
    
    def validate_password(self,value):#field level validation
        if len(value) < 2:
            raise serializers.ValidationError('Password must be 8 digit')
        return make_password(value) 
    
    def validate_test_types(self,value):#field level validation
        action = self.context['view'].action   
        
        if action == "update":
            if value != None:
                try:            
                    string = [int(id) for id in value.split(',')]
                    instance = self.instance
                    if instance.role == roles.ANALYST and len(string) <2:
                        return string
                    elif instance.role == roles.SUPERVISOR:
                        return string
                    else:
                        if instance.role == roles.ANALYST:
                            raise serializers.ValidationError('multiple test type not alowed')
                        else:
                            raise serializers.ValidationError('Test type allowed for only analyst and supervisor.')                
                except:
                    raise serializers.ValidationError('Test type unknown id')
            
                return string
        else:
            if value != None: #multiple test type not alowed' md blunder
                string = [int(id) for id in value.split(',')]
                
                return string
                # raise serializers.ValidationError('Test type allowed for only analyst and supervisor.')

        return value
      
    def validate_role(self,value):#field level validation
        user = self.context['request'].user
        if not user.is_authenticated:
            if value!=roles.USER:
                raise serializers.ValidationError("You can only set USER as role") 
        elif user.role==roles.SUPERADMIN:
            return value
        elif user.is_authenticated and value!=roles.USER:
                raise serializers.ValidationError("You can only set USER as role") 
        return value

    def validate_is_superuser(self,value):
        if value == True:
            raise serializers.ValidationError("You can not set USER as superadmin") 
        else:
            return False
    
    def validate(self, attrs):
        # print(attrs,"\n attrs...")
        request = self.context.get('request')
        action = self.context['view'].action     

        if action == 'partial_update' and 'is_verified' in attrs and 'remarks' in attrs:
            attrs['approved_by'] = request.user

        if action == 'partial_update':
            old_password = request.data.get('old_password')  
            if old_password is not None:      
                instance = self.instance
                if not instance.check_password(old_password):
                    raise serializers.ValidationError("Password does not match")
        return attrs
    
    approved_by = ApprovedBySerializer(read_only = True)

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        try:
            if self.context['request'].method == 'PUT':
                extra_kwargs['password'] = {'required': False}
            return extra_kwargs
        except:
            pass
    
    class Meta:
        ref_name =  "account serializer"
        model = CustomUser
        # fields = '__all__' 
        exclude = ['test_type']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        test_type = instance.test_type
        try:            
            string = [int(value) for value in test_type.split(',')]
        except:
            string = test_type
        #representation['test_type'] = string
        return representation


class RoleSerializer(serializers.Serializer):
    role_id = serializers.IntegerField()
    role_name = serializers.CharField()
    def to_representation(self, instance):
        return {'role_id': instance[0], 'role_name': instance[1]}
    
class departmentTypeSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    def to_representation(self, instance):
        return {'code': instance[0], 'name': instance[1]}

   
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'  

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'  

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()

class GroupNamesSerializer(serializers.Serializer):
    group_names = serializers.ListField(child=serializers.CharField())

class PermissionGroupSerializer(serializers.Serializer):
    permission_id = serializers.IntegerField()
    groups = serializers.DictField(child=serializers.BooleanField())
