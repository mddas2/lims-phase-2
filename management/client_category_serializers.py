from rest_framework import serializers
from management.models import ClientCategoryDetail,ClientCategoryDetailImages


class ClientCategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientCategoryDetail
        fields = '__all__'
    
    def validate(self, attrs):
        client_category = attrs.get('client_category')
        # raise serializers.ValidationError('testing sample form client category...')
        return super().validate(attrs)

class ClientCategoryDetailImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientCategoryDetailImages
        fields = '__all__'
    
    def validate(self, attrs):
      
        # raise serializers.ValidationError('testing sample form client category...')
        return super().validate(attrs)
