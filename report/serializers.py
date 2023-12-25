from management.models import ClientCategory, SampleForm, Commodity, CommodityCategory , TestResult ,SampleFormHasParameter,Payment,SampleFormParameterFormulaCalculate
from rest_framework import serializers
from account.models import CustomUser

class ClientCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientCategory
        fields = '__all__'        

class PaymentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Payment
            fields = '__all__' 

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'


class SampleFormManySerializer(serializers.ModelSerializer):
    parameters = TestResultSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = SampleForm
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        sample_form_id = representation.get('id')

        # Add extra response data for parameters field
        parameters_data = representation.get('parameters', [])
      
        for parameter_data in parameters_data:
            parameter_id = parameter_data.get('id')
            # Check if the parameter exists in SampleFormHasParameter model
            exists = SampleFormHasParameter.objects.filter(parameter=parameter_id, sample_form = sample_form_id).exists()
            parameter_data['exist'] = exists

        representation['parameters'] = parameters_data
        return representation

class SampleFormOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleForm
        fields = '__all__'

class CommodityManySerializer(serializers.ModelSerializer):
    test_result = TestResultSerializer(many=True,read_only=True)
    class Meta:
        model = Commodity
        fields = '__all__'

class CommodityOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = '__all__'
   
class CommodityCategorySerializer(serializers.ModelSerializer):
    def validate_name(self,value):#field level validation
        if value == "test":
            raise serializers.ValidationError('name test should not be there error')
        return value
    
    def validate(self, data):
        name = data.get('name')
        #id = data.get('id')
        if name == "test":
            raise serializers.ValidationError('name test should not be there error')
        return data
    
    commodity = CommodityOnlySerializer(many=True,read_only=True)
    class Meta:
        model = CommodityCategory
        fields = '__all__'

class SampleFormHasParameterReadSerializer(serializers.ModelSerializer):
    sample_form = SampleFormOnlySerializer(read_only=True)
    commodity = CommodityOnlySerializer(read_only=True)
    parameter = TestResultSerializer(many=True,read_only=True)
    class Meta:
        model = SampleFormHasParameter
        fields = '__all__' 


    def get_parameter(self, obj):
        parameter_data = TestResultSerializer(obj.parameter, many=True).data

        # Extract the parameter identifiers from obj.parameter
        # parameter_ids = [parameter['id'] for parameter in parameter_data]
        # print(parameter_ids)

        # Filter SampleFormParameterFormulaCalculate by commodity_id, parameter_ids, and sample_form_id
     
        # print(obj.parameter)
        for parameter in parameter_data:
            formula_calculate = SampleFormParameterFormulaCalculate.objects.filter(parameter = parameter['id'],sample_form=obj.sample_form_id).first()
            # formula_calculate = SampleFormParameterFormulaCalculate.objects.filter(commodity=obj.commodity_id,parameter = parameter['id'],sample_form=obj.sample_form_id).first()
            # print(obj.commodity_id)
            # print(parameter['id'])
            parameter['result'] = formula_calculate.result if formula_calculate else "10"
        return parameter_data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(instance.parameter.first().id)
        representation['parameter'] = self.get_parameter(instance)
        return representation

class SampleFormHasParameterWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleFormHasParameter
        fields = '__all__' 

class CustomUserSerializer(serializers.ModelSerializer):
    # client_category = ClientCategorySerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = '__all__' 