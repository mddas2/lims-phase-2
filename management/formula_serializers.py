from .models import SampleFormParameterFormulaCalculate,SampleFormVerifier
from rest_framework import serializers
from . encode_decode import generateDecodeIdforSampleForm,generateAutoEncodeIdforSampleForm

class SampleFormParameterFormulaCalculateReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleFormParameterFormulaCalculate
        fields = '__all__'

class FormulaApiCalculateSerializer(serializers.Serializer):
    commodity = serializers.IntegerField()#serializers.CharField()
    parameter = serializers.IntegerField()
    sample_form = serializers.IntegerField()
    formula_variable_fields_value = serializers.CharField()
    
    def to_internal_value(self, data):
        user = self.context['request'].user
     
        decoded_sample_form_id = generateDecodeIdforSampleForm(data['sample_form'],user)

        data['sample_form'] = decoded_sample_form_id

        return super().to_internal_value(data)

class FormulaApiCalculateSaveSerializer(serializers.Serializer):
    commodity = serializers.IntegerField()#serializers.CharField()
    parameter = serializers.IntegerField()
    sample_form = serializers.CharField()
    sample_form_has_parameter = serializers.IntegerField()
    result = serializers.CharField(allow_null = True,required=False,allow_blank=True,)
    formula_variable_fields_value = serializers.CharField(allow_null = True,required=False,allow_blank=True,)
    # remarks = formula_variable_fields_value = serializers.CharField()
    # analyst_remarks = serializers.CharField(blank = True)
    converted_result = serializers.CharField(allow_null = True,required=False,allow_blank=True,)
    decimal_place = serializers.CharField(allow_null = True,required=False,allow_blank=True,)

    units = serializers.CharField(allow_null = True,required=False,allow_blank=True,)
    mandatory_standard = serializers.CharField(allow_null = True,required=False,allow_blank=True)
    test_method = serializers.CharField(allow_null = True,required=False,allow_blank=True)
    additional_info = serializers.CharField(allow_null = True,required=False,allow_blank=True)

    
    def to_internal_value(self, data):
        user = self.context['request'].user
     
        decoded_sample_form_id = generateDecodeIdforSampleForm(data['sample_form'],user)

        data['sample_form'] = decoded_sample_form_id

        return super().to_internal_value(data)

class FormulaApiGetFieldSerializer(serializers.Serializer):
    commodity_id = serializers.IntegerField()
    parameter_id = serializers.IntegerField()
    sample_form_id = serializers.IntegerField()

    def to_internal_value(self, data):
        user = self.context['request'].user
     
        decoded_sample_form_id = generateDecodeIdforSampleForm(data['sample_form_id'],user)

        data['sample_form_id'] = decoded_sample_form_id

        return super().to_internal_value(data)



    def validate(self, data):
        commodity_id = data.get('commodity_id')
        parameter_id = data.get('parameter_id')
        sample_form_id = data.get('sample_form_id')

        # Perform your validation logic
        if commodity_id and parameter_id and sample_form_id:
            pass
            # Example validation condition
            # if commodity_id == 1 and parameter_id == 2 and sample_form_id == 3:
            #     raise serializers.ValidationError("Invalid combination of commodity, parameter, and sample form.")

        # Return the validated data
        return data
 
class RecheckSerializer(serializers.Serializer):
    parameter = serializers.IntegerField()
    sample_form = serializers.CharField()
    remarks = serializers.CharField()
    sample_form_has_parameter = serializers.IntegerField()

    # remarks = formula_variable_fields_value = serializers.CharField()
    
    def to_internal_value(self, data):
        user = self.context['request'].user
     
        decoded_sample_form_id = generateDecodeIdforSampleForm(data['sample_form'],user)

        data['sample_form'] = decoded_sample_form_id

        return super().to_internal_value(data)
    
    def validate(self, attrs):
        sample_form_id = attrs.get('sample_form')
        check_verifier = SampleFormVerifier.objects.filter(sample_form_id = sample_form_id).exists() #if already exists in verifier then no one can modified  put in serializer  validations
        if check_verifier:
            raise serializers.ValidationError('Sample Form already reached to Verifier so you can not modified')
        return super().validate(attrs)

class SampleFormRecheckSerializer(serializers.Serializer):
    sample_form = serializers.CharField()
    remarks = serializers.CharField()

    
    def to_internal_value(self, data):
        user = self.context['request'].user
     
        decoded_sample_form_id = generateDecodeIdforSampleForm(data['sample_form'],user)

        data['sample_form'] = decoded_sample_form_id

        return super().to_internal_value(data)