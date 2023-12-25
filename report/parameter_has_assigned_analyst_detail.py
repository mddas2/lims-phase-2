from management.models import Units,MandatoryStandard,ClientCategoryDetail,SampleForm, Commodity,SampleFormHasParameter,TestResult,SampleFormParameterFormulaCalculate,Payment
from rest_framework import serializers

from management.models import SampleForm, Commodity,SampleFormHasParameter,SuperVisorSampleForm
from account.models import CustomUser
from rest_framework import serializers
from management.encode_decode import generateDecodeIdforSampleForm,generateAutoEncodeIdforSampleForm
from management.status_naming import over_all_status
from management import roles

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','id','email','department_name','department_address','position'] 

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = ['name']

class SupervisorSampleFormSerializer(serializers.ModelSerializer):
    supervisor_user = CustomUserSerializer(read_only = True)
    class Meta:
        ref_name = "SupervisorSampleFormSerializer"
        model = SuperVisorSampleForm
        fields = ['supervisor_user','remarks','created_date']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "report_payment_detail"
        model = Payment
        fields = '__all__'
        depth = 1

class SampleFormHasParameterReadSerializer(serializers.ModelSerializer):
    analyst_user = CustomUserSerializer(read_only = True)
    class Meta:
        model = SampleFormHasParameter
        fields = ['analyst_user','created_date'] 

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'

class TestResultLimitedSerializer(serializers.ModelSerializer):
    # commodity = CommodityReadSerializer(many=False,read_only = True)

    class Meta:
        model = TestResult
        ref_name = "TestResultLimitedSerializer"
        exclude = ['units', 'mandatory_standard', 'test_method']


class DetailSampleFormHasParameterAnalystSerializer(serializers.ModelSerializer):
    commodity = CommoditySerializer(read_only = True)
    parameters = ParameterSerializer(read_only = True, many = True)
    owner_user = serializers.SerializerMethodField()
    supervisor_user = CustomUserSerializer(read_only = True)
    verified_by = CustomUserSerializer(read_only = True)
    class Meta:
        model = SampleForm
        fields = '__all__'
    
    def get_owner_user(self, obj):
        email = obj.owner_user
        try:
            user = CustomUser.objects.get(email=email)
            return CustomUserSerializer(user).data
        except CustomUser.DoesNotExist:
            return None


    def to_representation(self, instance):
        request = self.context.get('request')
        user = request.user
        representation = super().to_representation(instance)

        sample_form_id = representation.get('id')

        normal_status = representation.get('status')
        if normal_status == "not_assigned":
            representation['status'] = "Processing"

        # Add extra response data for parameters field
        parameters_data = representation.get('parameters', [])
        sample_form_has_param_id = None
        params_data_fixed = []
        for param in parameters_data:
            parameter_id = param.get('id')
            obk = SampleFormHasParameter.objects.filter(parameter=parameter_id, sample_form = sample_form_id,analyst_user=user)
            exists = obk.exists()
            if exists:
                sample_form_has_param_id = obk.first().id
                params_data_fixed.append(param)    

        parameters_data = params_data_fixed
      
        for parameter_data in parameters_data:
            parameter_id = parameter_data.get('id')
           
            sample_form_has_assigned_analyst_obj = SampleFormHasParameter.objects.filter(parameter=parameter_id, sample_form = sample_form_id,analyst_user=user)
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
                
                # sup_full_name = analyst_obj.super_visor_sample_form#.supervisor_user.first_name
    
                parameter_data['sup_full_name'] = str(sample_form_has_assigned_analyst_obj.first().super_visor_sample_form.supervisor_user.first_name)+" "+ str(sample_form_has_assigned_analyst_obj.first().super_visor_sample_form.supervisor_user.last_name)#blundermd
                
                formula_obj_result = SampleFormParameterFormulaCalculate.objects.filter(sample_form_id=sample_form_id,parameter_id = parameter_id)
                if formula_obj_result.count()>0:
                    parameter_data['status'] = formula_obj_result.first().status
                    parameter_data['result'] = formula_obj_result.first().result

                    parameter_data['analyst_remarks'] = formula_obj_result.first().analyst_remarks

                    parameter_data['units'] = formula_obj_result.first().units
                    parameter_data['mandatory_standard'] = formula_obj_result.first().mandatory_standard
                    parameter_data['test_method'] = formula_obj_result.first().test_method
                else:
                    parameter_data['status'] = "processing"
                    parameter_data['result'] = '-'
            else:
                parameters_data.remove(parameter_data) 

            parameter_data['exist'] = exists

        representation['parameters'] = parameters_data
        representation['sample_form_has_param_id'] = sample_form_has_param_id

        client_category_detail = instance.client_category_detail.client_category.id
        if client_category_detail == 11:
            representation['name'] = instance.commodity.name #"error md fix" #sample_name
        representation['client_category'] = client_category_detail

        return representation


class DetailSampleFormHasParameterRoleAsAnalystSerializer_Temp(serializers.ModelSerializer):
    commodity = CommoditySerializer(read_only = True)
    
    parameters = TestResultLimitedSerializer(read_only = True, many = True)
    
    owner_user = serializers.SerializerMethodField()
    verified_by = CustomUserSerializer(read_only = True)
    approved_by = CustomUserSerializer(read_only = True)

    supervisor_sample_form = SupervisorSampleFormSerializer(many = True,read_only = True)

    payment = PaymentSerializer(read_only = True,many = True)

    
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)
    
    class Meta:
        model = SampleForm
        fields = '__all__'
    
    def get_owner_user(self, obj):
        email = obj.owner_user
        try:
            user = CustomUser.objects.get(email=email)
            return CustomUserSerializer(user).data
        except CustomUser.DoesNotExist:
            return None


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        sample_form_id = representation.get('id')
        sample_form_id = generateDecodeIdforSampleForm(sample_form_id,self.context['request'].user)

        # Add extra response data for parameters field
        parameters_data = representation.get('parameters', [])

        user = self.context['request'].user

        # representation['status'] = over_all_status[representation.get('status')]
        if user.role == roles.SMU or user.role == roles.SUPERADMIN:
            smu_superadmin_status = representation.get('status')
            representation['status'] = over_all_status[smu_superadmin_status]
            # if smu_superadmin_status == "not_assigned" or smu_superadmin_status == "not_verified":
            #     representation['status'] = "processing"
        

        elif user.role == roles.USER:
            
            pass
            # representation['payment'] = PaymentSerializer(instance.payment).data

        for parameter_data in parameters_data:
            parameter_id = parameter_data.get('id')
            # Check if the parameter exists in SampleFormHasParameter model
            # print(parameter_id)
            if user.role == roles.SMU or user.role == roles.SUPERADMIN or user.role == roles.VERIFIER or user.role == roles.ADMIN:
                sample_form_has_supervisor_obj = SuperVisorSampleForm.objects.filter(parameters=parameter_id, sample_form = sample_form_id)
                exists_sup = sample_form_has_supervisor_obj.exists()
                if exists_sup:
                    sup_full_name = str(sample_form_has_supervisor_obj.first().supervisor_user.first_name) +' '+ str(sample_form_has_supervisor_obj.first().supervisor_user.last_name)
                    # parameter_data['sup_full_name'] = 'ask with manoj das'
                    parameter_data['sup_full_name'] = sup_full_name

            sample_form_has_assigned_analyst_obj = SampleFormHasParameter.objects.filter(parameter=parameter_id, sample_form = sample_form_id)
            exists = sample_form_has_assigned_analyst_obj.exists()
            if exists:
                analyst_obj = sample_form_has_assigned_analyst_obj.first().analyst_user
                first_name = analyst_obj.first_name
                last_name = analyst_obj.last_name
                status = sample_form_has_assigned_analyst_obj.first().status
                created_date = sample_form_has_assigned_analyst_obj.first().created_date
                parameter_data['first_name'] = first_name
                parameter_data['last_name'] = last_name
                
                parameter_data['sample_form_has_parameter'] = sample_form_has_assigned_analyst_obj.first().id  
                parameter_data['assigned_date'] = created_date
                
                formula_obj_result = SampleFormParameterFormulaCalculate.objects.filter(sample_form_id=sample_form_id,parameter_id = parameter_id)
                if formula_obj_result.count()>0:
                    parameter_data['status'] = formula_obj_result.first().status
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
                    parameter_data['status'] = "processing"
                    parameter_data['result'] = '-'


            parameter_data['exist'] = exists

        representation['parameters'] = parameters_data

        try:
            representation['analysis_completed_date'] = instance.sample_has_parameter_analyst.all().order_by('-completed_date').first().completed_date
        except:
            representation['analysis_completed_date'] = ''
        
        try:
            representation['analysis_started_date'] = instance.sample_has_parameter_analyst.all().order_by('id').first().started_date
        except:
            representation['analysis_started_date'] = '-'
        
        client_category_detail = instance.client_category_detail.client_category.id
        if client_category_detail == 11:
            representation['name'] = instance.commodity.name #"error md fix" #sample_name
        representation['client_category'] = client_category_detail

        return representation



class ClientCategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "ClientCategoryDetailSerializer"
        model = ClientCategoryDetail
        fields = '__all__'

class FinalReportNepaliAnalystSerializer(serializers.ModelSerializer):
    commodity = CommoditySerializer(read_only = True)
    parameters = TestResultLimitedSerializer(read_only = True, many = True)
    owner_user = serializers.SerializerMethodField()
    supervisor_user = CustomUserSerializer(read_only = True)
    verified_by = CustomUserSerializer(read_only = True)
    approved_by = CustomUserSerializer(read_only = True)
    client_category_detail = ClientCategoryDetailSerializer(read_only = True,many=False)
    
    
    class Meta:
        model = SampleForm
        fields = '__all__'
    
    def get_owner_user(self, obj):
        email = obj.owner_user
        try:
            user = CustomUser.objects.get(email=email)
            return CustomUserSerializer(user).data
        except CustomUser.DoesNotExist:
            return None


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        sample_form_id = representation.get('id')

        # Add extra response data for parameters field
        parameters_data = representation.get('parameters', [])

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
                status = sample_form_has_assigned_analyst_obj.first().status
                created_date = sample_form_has_assigned_analyst_obj.first().created_date
                parameter_data['first_name'] = first_name
                parameter_data['last_name'] = last_name
                parameter_data['sample_form_has_parameter'] = sample_form_has_assigned_analyst_obj.first().id
                parameter_data['assigned_date'] = created_date
                
                formula_obj_result = SampleFormParameterFormulaCalculate.objects.filter(sample_form_id=sample_form_id,parameter_id = parameter_id)
                if formula_obj_result.count()>0:
                    parameter_data['status'] = formula_obj_result.first().status

                    analyst_remarks = formula_obj_result.first().analyst_remarks
                    
                    if analyst_remarks:
                        parameter_data['result'] = formula_obj_result.first().analyst_remarks
                    elif formula_obj_result.first().converted_result:
                        parameter_data['result'] = formula_obj_result.first().converted_result
                    else:
                        parameter_data['result'] = formula_obj_result.first().result

                    unit_obj = Units.objects.filter(units = formula_obj_result.first().units)
                    if unit_obj.count()>0:
                        parameter_data['units_selected'] = unit_obj.first().units_nepali
                        parameter_data['units_selected_en'] = formula_obj_result.first().units
                    else:
                        parameter_data['units_selected'] = formula_obj_result.first().units
                        parameter_data['units_selected_en'] = formula_obj_result.first().units
                    
                    mandatory_obj = MandatoryStandard.objects.filter(mandatory_standard = formula_obj_result.first().mandatory_standard)
                    if mandatory_obj.count()>0:
                        parameter_data['mandatory_standard_selected'] = mandatory_obj.first().mandatory_standard_nepali
                        parameter_data['mandatory_standard_selected_en'] = formula_obj_result.first().mandatory_standard
                    else:
                        parameter_data['mandatory_standard_selected'] = formula_obj_result.first().mandatory_standard
                        parameter_data['mandatory_standard_selected_en'] = formula_obj_result.first().mandatory_standard

                    parameter_data['test_method_selected'] = formula_obj_result.first().test_method
                else:
                    parameter_data['status'] = "processing"
                    parameter_data['result'] = '-'


            parameter_data['exist'] = exists

        representation['parameters'] = parameters_data
   

        try:
            representation['analysis_completed_date'] = instance.sample_has_parameter_analyst.all().order_by('-completed_date').first().completed_date
        except:
            representation['analysis_completed_date'] = ''
        
        try:
            representation['analysis_started_date'] = instance.sample_has_parameter_analyst.all().order_by('id').first().started_date
        except:
            representation['analysis_started_date'] = '-'

        client_category_detail = instance.client_category_detail.client_category.id
        if client_category_detail == 11:
            representation['name'] = instance.commodity.name #"error md fix" #sample_name
            
        return representation