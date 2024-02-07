from management.models import SampleForm, Commodity,SampleFormHasParameter,TestResult,SampleFormParameterFormulaCalculate
from rest_framework import serializers

from management.models import SampleForm, Commodity,SampleFormHasParameter
from account.models import CustomUser
from rest_framework import serializers
from management.encode_decode import generateDecodeIdforSampleForm,generateAutoEncodeIdforSampleForm

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'CustomUser_finalreport'
        model = CustomUser
        fields = ['first_name','last_name','id'] 

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'Commodity_finalreport'
        model = Commodity
        fields = ['name']

class SampleFormHasParameterReadSerializer(serializers.ModelSerializer):
    analyst_user = CustomUserSerializer(read_only = True)
    class Meta:
        ref_name = 'SampleFormHasParameter_finalreport'
        model = SampleFormHasParameter
        fields = ['analyst_user','created_date'] 

class CompletedSampleFormHasAnalystSerializer(serializers.ModelSerializer):
    sample_has_parameter_analyst = SampleFormHasParameterReadSerializer(many=True,read_only=True)
    commodity = CommoditySerializer(read_only = True)
    supervisor_user = CustomUserSerializer(read_only=True)

    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)
    
    class Meta:
        model = SampleForm
        fields = ['id','name','supervisor_user','sample_has_parameter_analyst','commodity','status','created_date','namuna_code']
    
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        client_category_detail = instance.client_category_detail.client_category.id
        if client_category_detail == 11:
            representation['name'] = instance.commodity.name #"error md fix" #sample_name
        return representation

class DetailSampleFormHasParameterRoleAsAnalystSerializer(serializers.ModelSerializer):
    commodity = CommoditySerializer(read_only=True)
    parameters = ParameterSerializer(read_only=True, many=True)

    class Meta:
        model = SampleForm
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        sample_form_id = representation.get('id')
        parameters_data = representation.get('parameters', [])

        request = self.context.get('request')
        user = request.user if request else None

        filtered_parameters_data = []
        for parameter_data in parameters_data:
            parameter_id = parameter_data.get('id')

            sample_form_has_assigned_analyst_obj = SampleFormHasParameter.objects.filter(
                parameter=parameter_id, sample_form=sample_form_id, analyst_user=user
            )
            exists = sample_form_has_assigned_analyst_obj.exists()
            if exists:
                analyst_obj = sample_form_has_assigned_analyst_obj.first().analyst_user
                first_name = analyst_obj.first_name
                last_name = analyst_obj.last_name
                status = sample_form_has_assigned_analyst_obj.first().status
                created_date = sample_form_has_assigned_analyst_obj.first().created_date
                parameter_data['first_name'] = first_name
                parameter_data['last_name'] = last_name
                parameter_data['assigned_date'] = created_date

                formula_obj_result = SampleFormParameterFormulaCalculate.objects.filter(
                    sample_form_id=sample_form_id, parameter_id=parameter_id
                )
                if formula_obj_result.count() > 0:
                    parameter_data['status'] = "completed"
                    parameter_data['result'] = formula_obj_result.first().result
                else:
                    parameter_data['status'] = "processing"
                    parameter_data['result'] = '-'

                parameter_data['exist'] = exists
                filtered_parameters_data.append(parameter_data)

        representation['parameters'] = filtered_parameters_data
        return representation
