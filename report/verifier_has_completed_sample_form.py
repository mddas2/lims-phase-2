from management.models import SampleForm, Commodity,SampleFormHasParameter
from rest_framework import serializers

from management.models import SampleForm, Commodity,SampleFormHasParameter
from account.models import CustomUser
from rest_framework import serializers
from management.encode_decode import generateDecodeIdforSampleForm,generateAutoEncodeIdforSampleForm

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','id'] 

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = ['name']

class SampleFormHasParameterReadSerializer(serializers.ModelSerializer):
    analyst_user = CustomUserSerializer(read_only = True)
    class Meta:
        ref_name = "SampleFormHasParameterReadSerializer_verifier"
        model = SampleFormHasParameter
        fields = ['analyst_user','created_date'] 

class CompletedSampleFormHasVerifierSerializer(serializers.ModelSerializer):
    sample_has_parameter_analyst = SampleFormHasParameterReadSerializer(many=True,read_only=True)
    commodity = CommoditySerializer(read_only = True)
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)
    class Meta:
        model = SampleForm
        fields = ['id','name','sample_has_parameter_analyst','commodity','status','created_date','sample_lab_id','namuna_code']
        ref_name = "verifier_CompletedSampleFormHasVerifierSerialize"