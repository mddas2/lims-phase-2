from management.models import ClientCategory, SampleForm
from account.models import CustomUser
from rest_framework import serializers


class SampleFormSerializer(serializers.ModelSerializer): #this is  for data filter by sagar
    # client_category = ClientCategorySerializer(read_only=True)
    ref_name = "AdditionalSampleFormSerializer"
    class Meta:
        model = SampleForm
        fields = ['id','owner_user']
    
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        user_obj = CustomUser.objects.filter(email = instance.owner_user).first()
    
        representation['number'] = user_obj.phone
        representation['user_name'] = user_obj.username
        representation['client_category'] = user_obj.client_category.name
        representation['department_name'] = user_obj.department_name
        representation['department_address'] = user_obj.department_address

        return representation


