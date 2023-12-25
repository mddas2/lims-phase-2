from management.models import SampleForm, Commodity,SampleFormHasParameter,TestResult
from rest_framework import serializers

from management.models import SampleForm, Commodity,SampleFormHasParameter,SampleFormParameterFormulaCalculate
from account.models import CustomUser
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','id','test_type'] 

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = ['name']

class SampleFormHasParameterReadSerializer(serializers.ModelSerializer):
    analyst_user = CustomUserSerializer(read_only = True)
    class Meta:
        model = SampleFormHasParameter
        fields = ['analyst_user','created_date'] 

class SampleFormTrackbyAnalystSerializer(serializers.ModelSerializer):
    analyst_user = CustomUserSerializer(read_only = True)
    class Meta:
        model = SampleFormHasParameter
        fields = ['analyst_user','status','created_date'] 

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ['id','name']

class SampleFormHasParameterAnalystSerializer(serializers.ModelSerializer):
    commodity = CommoditySerializer(read_only = True)
    parameters = ParameterSerializer(read_only = True, many = True)
    class Meta:
        model = SampleForm
        fields = ['id','name','parameters','commodity','status','created_date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        sample_form_id = representation.get('id')

        # Add extra response data for parameters field
        parameters_data = representation.get('parameters', [])
        stat = "processing"
        for parameter_data in parameters_data:
            parameter_id = parameter_data.get('id')
            # Check if the parameter exists in SampleFormHasParameter model
            # print(parameter_id)
            sample_form_has_assigned_analyst_obj = SampleFormHasParameter.objects.filter(parameter=parameter_id, sample_form = sample_form_id)
            exists = sample_form_has_assigned_analyst_obj.exists()
            if exists:
                analyst_obj = sample_form_has_assigned_analyst_obj.first().analyst_user
                first_name = analyst_obj.first_name
                last_name = analyst_obj.last_name
                # status = sample_form_has_assigned_analyst_obj.first().status
                created_date = sample_form_has_assigned_analyst_obj.first().created_date
                parameter_data['first_name'] = first_name
                parameter_data['last_name'] = last_name
                parameter_data['assigned_date'] = created_date

                formula_obj_result = SampleFormParameterFormulaCalculate.objects.filter(sample_form_id=sample_form_id,parameter_id = parameter_id)
                if formula_obj_result.count()>0:
                    stat = "completed"
                    parameter_data['status'] = "completed"
                    parameter_data['result'] = formula_obj_result.first().result
                else:
                    stat = "processing"
                    parameter_data['status'] = "processing"
                    parameter_data['result'] = '-'
                # parameter_data['status'] = "completed"

            parameter_data['exist'] = exists

        representation['parameters'] = parameters_data
        representation['status'] = stat
        return representation
