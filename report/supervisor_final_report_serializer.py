from rest_framework import serializers
from management.models import SuperVisorSampleForm,ClientCategory, SampleForm, Commodity, CommodityCategory , TestResult ,SampleFormHasParameter,Payment,SampleFormParameterFormulaCalculate
from account.models import CustomUser

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "supervisorfinalreportTestResult"
        model = TestResult
        fields = '__all__'

class SampleFormSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "supervisorfinalreportSampleform"
        model = SampleForm
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "supervisorfinalreportCustomUserSerializer"
        model = CustomUser
        fields = ['first_name','last_name']

class SupervisorFinalReportSerializer(serializers.ModelSerializer):
    parameters = TestResultSerializer(read_only = True,many=True)
    sample_form = SampleFormSerializer(read_only = True)
    supervisor_user = CustomUserSerializer(read_only = True)
    class Meta:
        ref_name = "supervisorfinalreportSuperVisorSampleForm"
        model = SuperVisorSampleForm
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        sample_form_id = representation.get('sample_form')['id']
      
        # Add extra response data for parameters fieldo
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
                    parameter_data['analyst_remarks'] = formula_obj_result.first().analyst_remarks #formula_obj_result.first().test_method

                    analyst_remarks = formula_obj_result.first().analyst_remarks
                    
                    if analyst_remarks:
                        parameter_data['result'] = formula_obj_result.first().analyst_remarks
                    elif formula_obj_result.first().converted_result:
                        parameter_data['result'] = formula_obj_result.first().converted_result
                    else:
                        parameter_data['result'] = formula_obj_result.first().result

                    parameter_data['units'] = formula_obj_result.first().units
                    parameter_data['mandatory_standard'] = formula_obj_result.first().mandatory_standard
                    parameter_data['test_method'] = formula_obj_result.first().test_method
                else:
                    stat = "processing"
                    parameter_data['status'] = "processing"
                    parameter_data['result'] = '-'
                # parameter_data['status'] = "completed"

            parameter_data['exist'] = exists

        representation['parameters'] = parameters_data
        representation['status'] = stat
        return representation


    