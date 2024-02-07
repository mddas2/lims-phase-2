from .models import FiscalYear,Units,MandatoryStandard,TestMethod,MicroObservationTable,ClientCategory,SuperVisorSampleForm,ClientCategoryDetailImages, SampleForm, Commodity, CommodityCategory, MicroParameter , TestResult ,SampleFormHasParameter,Payment,SampleFormParameterFormulaCalculate,ClientCategoryDetail,NoticeImages,VerifiedList,ApprovedList,SampleFormVerifier
from rest_framework import serializers
from account.models import CustomUser
from . import roles
from . encode_decode import generateDecodeIdforSampleForm,generateAutoEncodeIdforSampleForm
from . raw_data import generateRawData,UpdategenerateRawData
from .status_naming import over_all_status
from django.utils import timezone
import ast

class FiscalYearSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "FiscalYearSerializer"
        model = FiscalYear
        fields = '__all__'

class ApprovedBySerializer(serializers.ModelSerializer):
     class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','id','department_name'] 

class ApprovedByListSerializer(serializers.ModelSerializer):
     class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','id','position'] 

class ClientCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientCategory
        fields = '__all__'        

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__' 
        

class CommodityReadSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "CommodityRead_management"
        model = Commodity
        fields = ['id','name','name_nepali']

class UnitsReadSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "UnitsReadSerializer"
        model = Units
        fields = '__all__'
        
class MandatoryStandardReadSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "MandatoryStandardReadSerializer"
        model = MandatoryStandard
        fields = '__all__'

class TestMethodReadSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "TestMethodReadSerializer"
        model = TestMethod
        fields = '__all__'

class TestResultSerializer(serializers.ModelSerializer):
    commodity = CommodityReadSerializer(many=False,read_only = True)

    units = UnitsReadSerializer(many=True,read_only = True)
    mandatory_standard = MandatoryStandardReadSerializer(many=True,read_only = True)
    test_method = TestMethodReadSerializer(many=True,read_only = True)

    class Meta:
        model = TestResult
        fields = '__all__'


class TestResultForSampleFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ['id']

class TestResultLimitedSerializer(serializers.ModelSerializer):
    commodity = CommodityReadSerializer(many=False,read_only = True)

    class Meta:
        model = TestResult
        exclude = ['units', 'mandatory_standard', 'test_method','formula','price']

class TestResultOnlySerializerRead(serializers.ModelSerializer):
    class Meta:
        ref_name = "TestResultOnlySerializerRead"
        model = TestResult
        fields = ['id','name','price']
    
class TestResultWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'


class CommoditySerializer(serializers.ModelSerializer):
    test_result = TestResultSerializer(many=True,read_only=True)
    class Meta:
        ref_name = "Commodity_management"
        model = Commodity
        fields = '__all__'

class CommoditySampleFormSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "Commodity_management"
        model = Commodity
        fields = ['name','id']

class ClientCategoryDetailImagesSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "ClientCategoryDetailImagesSerializer"
        model = ClientCategoryDetailImages
        fields = '__all__'

class ClientCategoryDetailSerializer(serializers.ModelSerializer):
    ClientCategoryDetail = ClientCategoryDetailImagesSerializer(many=True,read_only=True)
    class Meta:
        ref_name = "ClientCategoryDetailSerializer"
        model = ClientCategoryDetail
        fields = '__all__'


class limitedCommidityCategoryreadSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "limitedCommidityCategoryreadSerializer"
        model = CommodityCategory
        fields = ['id','name']

class limitedCommidityreadSerializer(serializers.ModelSerializer):
    test_result = TestResultOnlySerializerRead(many=True,read_only=True)
    class Meta:
        ref_name = "limitedCommidityreadSerializer"
        model = Commodity
        fields = ['id','name','price','test_result','test_duration','name_nepali']
        

class MicroObservationTableSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        if 'sample_form' in data:
            sample_form_id = data['sample_form'] 
            decoded_sample_form_id = generateDecodeIdforSampleForm(sample_form_id,self.context['request'].user)#smart_text(urlsafe_base64_decode(data['sample_form']))
            data['sample_form'] = decoded_sample_form_id
        return super().to_internal_value(data)
    
    class Meta:
        model = MicroObservationTable
        fields = '__all__' 
    

class MicroParameterSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        action = self.context['view'].action
        #print("action .... ", action)
        if 'sample_form' in data and action != "update":
            sample_form_id = data['sample_form'] 
            decoded_sample_form_id = generateDecodeIdforSampleForm(sample_form_id,self.context['request'].user)#smart_text(urlsafe_base64_decode(data['sample_form']))
            data['sample_form'] = decoded_sample_form_id
        return super().to_internal_value(data)
    micro_observation_table = MicroObservationTableSerializer(many = True,read_only = True)
    class Meta:
        model = MicroParameter 
        fields = '__all__' 
    
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['parameter_name'] = instance.parameter.name
        return representation


# class CommoditySerializer(serializers.ModelSerializer):
#     class Meta:
#         ref_name = "Commodity_sample_form"
#         model = Commodity
#         fields = '__all__


class SampleFormListSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)

    # parameters = TestResultForSampleFormSerializer(many=True, read_only=True)

    owner_user = serializers.SerializerMethodField()

    supervisor_user = ApprovedBySerializer(read_only = True)

    commodity = CommoditySampleFormSerializer(read_only = True,many=False)

    client_category_detail = ClientCategoryDetailSerializer(read_only = True,many=False)
    
    class Meta:
        supervisor_user = ApprovedBySerializer(read_only = True)
        model = SampleForm
        fields = ['id','owner_user','name','new_name','commodity','supervisor_user','parameters','refrence_number','sample_lab_id','remarks','remarks_recheck_verifier','remarks_reject_verifier','admin_remarks','verifier_remarks','client_category_detail','status','namuna_code','created_date']

    def get_owner_user(self, obj):
        email = obj.owner_user
        try:
            user = CustomUser.objects.get(email=email)
            return ApprovedBySerializer(user).data
        except CustomUser.DoesNotExist:
            return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # sample_form_id = representation.get('id')
        # sample_form_id = generateDecodeIdforSampleForm(sample_form_id,self.context['request'].user)

        # parameters_data = representation.get('parameters', [])
        assigned = 0
        # for parameter_data in parameters_data:
        #     parameter_id = parameter_data
        #     # Check if the parameter exists in SampleFormHasParameter model
        #     smple_frm_exist = SampleFormHasParameter.objects.filter(parameter=parameter_id, sample_form = sample_form_id)
        #     exists = smple_frm_exist.exists()
        #     parameter_data['exist'] = exists

        #     smple_frm_exist_for_supervisor = SuperVisorSampleForm.objects.filter(parameters=parameter_id, sample_form = sample_form_id)
        #     exists_supervisor_parameter = smple_frm_exist_for_supervisor.exists()
        #     parameter_data['exists_supervisor_parameter'] = exists_supervisor_parameter

        #     if exists_supervisor_parameter:
        #         # print(smple_frm_exist.first().analyst_user.username)
        #         try:
        #             parameter_data['status_supervisor'] = "assigned"
        #             parameter_data['supervisor_user'] = smple_frm_exist_for_supervisor.first().supervisor_user.username
        #         except:
        #             pass 

        #     if exists:
        #         # print(smple_frm_exist.first().analyst_user.username)
        #         try:
        #             parameter_data['status'] = "assigned"
        #             parameter_data['analyst'] = smple_frm_exist.first().analyst_user.username
        #         except:
        #             pass           


        #     if exists == True:
        #         assigned+=1

        representation['total_assign'] = '-'#assigned
        representation['parameters'] = ''
        
        status = representation.get('status')
        request = self.context.get('request')

        if request.user.role == roles.USER:
            if status == "pending" or status == "processing" or status=="completed" or status == "recheck":
                representation['status'] = status
            else:
                representation['status'] = "processing"
                
        if request.user.role == roles.SUPERVISOR:
            if status == "not_assigned":
                representation['status'] = "Not Assigned"

        return representation

class SampleFormReadSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)

    parameters = TestResultSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True,many=True)

    owner_user = serializers.SerializerMethodField()
    approved_by = ApprovedBySerializer(read_only = True,many=False)
    verified_by = ApprovedBySerializer(read_only = True,many=False)
    supervisor_user = ApprovedBySerializer(read_only = True)

    commodity = CommoditySerializer(read_only = True,many=False)

    client_category_detail = ClientCategoryDetailSerializer(read_only = True,many=False)
    
    class Meta:
        approved_by = ApprovedBySerializer(read_only = True)
        supervisor_user = ApprovedBySerializer(read_only = True)
        verified_by = ApprovedBySerializer(read_only = True)
        model = SampleForm
        fields = '__all__'

    def get_owner_user(self, obj):
        email = obj.owner_user
        try:
            user = CustomUser.objects.get(email=email)
            return ApprovedBySerializer(user).data
        except CustomUser.DoesNotExist:
            return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        sample_form_id = representation.get('id')
        sample_form_id = generateDecodeIdforSampleForm(sample_form_id,self.context['request'].user)

        parameters_data = representation.get('parameters', [])

        assigned = 0
        for parameter_data in parameters_data:
            parameter_id = parameter_data.get('id')
            # Check if the parameter exists in SampleFormHasParameter model
            smple_frm_exist = SampleFormHasParameter.objects.filter(parameter=parameter_id, sample_form = sample_form_id)
            exists = smple_frm_exist.exists()
            parameter_data['exist'] = exists

            smple_frm_exist_for_supervisor = SuperVisorSampleForm.objects.filter(parameters=parameter_id, sample_form = sample_form_id)
            exists_supervisor_parameter = smple_frm_exist_for_supervisor.exists()
            parameter_data['exists_supervisor_parameter'] = exists_supervisor_parameter

            if exists_supervisor_parameter:
                # print(smple_frm_exist.first().analyst_user.username)
                try:
                    parameter_data['status_supervisor'] = "assigned"
                    parameter_data['supervisor_user'] = smple_frm_exist_for_supervisor.first().supervisor_user.username
                except:
                    pass 

            if exists:
                # print(smple_frm_exist.first().analyst_user.username)
                try:
                    parameter_data['status'] = "assigned"
                    parameter_data['analyst'] = smple_frm_exist.first().analyst_user.username
                except:
                    pass           


            if exists == True:
                assigned+=1

        representation['total_assign'] = assigned
        representation['parameters'] = parameters_data
        
        status = representation.get('status')
        request = self.context.get('request')

        if request.user.role == roles.USER:
            if status == "pending" or status == "processing" or status=="completed" or status == "recheck":
                representation['status'] = status
            else:
                representation['status'] = "processing"
                
        if request.user.role == roles.SUPERVISOR:
            if status == "not_assigned":
                representation['status'] = "Not Assigned"


        return representation



class SampleFormWriteSerializer(serializers.ModelSerializer):
    
    def to_internal_value(self, data):
        action = self.context['view'].action
        if action != "partial_update":
            # Create a mutable copy of the QueryDict and convert it to a regular dictionary
            mutable_data = data.dict()
            parameters = mutable_data['parameters']        
            converted_list = ast.literal_eval(parameters)

            mutable_data['parameters'] = converted_list

            return super().to_internal_value(mutable_data)
        else:
            return super().to_internal_value(data)
    
    def validate_price(self,value):#field level validation
        raise serializers.ValidationError('price can not be modified error')
    
    # def validate_status(self,value):#field level validation
    #     sample_form_id = self.instance.id
    #     supervisor_data = SuperVisorSampleForm.objects.filter(sample_form_id = sample_form_id).exists()
    #     if supervisor_data == True and value == "recheck":
    #         raise serializers.ValidationError('sample form is assigned to supervisor so you can not Recheck. Error code E-SAMPLE-FORM-5')

    
    def validate_owner_user_obj(self,value):#field level validation
        raise serializers.ValidationError('owner_user_obj can not be modified error')
        
    def validate(self, data):
        # raise serializers.ValidationError('testing sample form dftqc')
        parameters = data.get('parameters')
        action = self.context['view'].action
        request = self.context.get('request')

        if action == "create":
            owner_user_id = CustomUser.objects.get(email = data.get('owner_user')).id
            data['owner_user_obj_id'] = owner_user_id
            data['created_by_user_id'] = request.user.id

        if action == "update" or action == "partial_update":
            if parameters and (request.user.role != roles.SMU and request.user.role != roles.USER):
                raise serializers.ValidationError('You have not permission to update parameters. Error code E-SAMPLE-FORM-1')
            
            sample_form_id = self.instance.id
            supervisor_data = SuperVisorSampleForm.objects.filter(sample_form_id = sample_form_id).exists()
            if supervisor_data and parameters: #if sampleform  reach to supervisor , then no one can update parameters.
                raise serializers.ValidationError('You have not permission to update parameters as sample is forwarded to lab. Error code E-SAMPLE-FORM-4')
            
        if action == "create" or action=="update": #user , smu
            commodity = data.get('commodity')

            commodity_parameters = TestResult.objects.filter(commodity=commodity)
            commodity_price = Commodity.objects.get(id = commodity.id).price
        
            if len(parameters) == 0:  
                data['parameters'] = commodity_parameters
            
            if data.get('analysis_pricing') == False:      
                data['price'] = commodity_price
            else:
                price = 0
                for paramet in data.get('parameters'):
                    price = paramet.price + price
                data['price'] = price
            return data
        
        if action == "partial_update":
            if request.user.role == roles.ADMIN:
                if len(data) == 2 and 'status' in data and 'admin_remarks' in data:
                    request = self.context.get('request')
                    print(request.data)
                    approved_by = CustomUser.objects.all().filter(id = int(request.data.get('approve_by')))
                    if approved_by.exists() == False:
                        raise serializers.ValidationError("Verified by user must be exists")    
                    data['approved_by_id'] = approved_by.first().id
                    return data
                else:
                    raise serializers.ValidationError('You have not permission. Error code E-SAMPLE-FORM-2')
            elif request.user.role == roles.VERIFIER:
                return data #blunder md blunder_md  hints more validate
            elif request.user.role == roles.SUPERVISOR:
                return data #blunder md blunder_md  hints more validate
            elif request.user.role == roles.SMU:
                return data #blunder md blunder_md  hints more validate
            else:
                raise serializers.ValidationError('You have not permission.Error code E-SAMPLE-FORM-3 ')
            #for verifier validate.
                    

        
    class Meta:
        model = SampleForm
        fields = '__all__'

    def get_fields(self):
        fields = super(SampleFormWriteSerializer, self).get_fields()
        # Check if the request method is PUT or PATCH
        request = self.context.get('request')
        if request and request.method in ['PUT', 'PATCH']:
            fields['owner_user'].read_only = True
            fields['owner_user_obj'].read_only = True
            fields['price'].read_only = True

        return fields

class SampleFormReadAnalystSerializer(serializers.ModelSerializer):
    commodity = CommodityReadSerializer(read_only=True,many=False)
    owner_user = serializers.SerializerMethodField()
    supervisor_user = ApprovedBySerializer(read_only = True)

    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)

    def validate(self, data):
        action = self.context['view'].action
        if action == "create":
            parameters = data.get('parameters')
            
            #id = data.get('id')
            if len(parameters) == 0:
                commodity = data.get('commodity')   
                parameters = TestResult.objects.filter(commodity=commodity)
                data['parameters'] = parameters
            return data
        else:
            return data
    def to_representation(self, instance): #if dftqc then sample name as commodity category else do no things
        representation = super().to_representation(instance)
        client_category_detail = instance.client_category_detail.client_category.id
        if client_category_detail == 11:
            representation['name'] = instance.commodity.name #"error md fix" #sample_name
        representation['client_category'] = client_category_detail
        return representation
        
    def get_owner_user(self, obj):
        email = obj.owner_user
        try:
            user = CustomUser.objects.get(email=email)
            return ApprovedBySerializer(user).data
        except CustomUser.DoesNotExist:
            return None

    class Meta:
        
        model = SampleForm
        fields = '__all__'

class CommodityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "CommodityCategorySerializerm"
        model = CommodityCategory
        fields = '__all__'

class CommodityAllReadSerializer(serializers.ModelSerializer):
    category = CommodityCategorySerializer(serializers.ModelSerializer)
    class Meta:
        model = Commodity
        fields = '__all__'

class CommodityWriteSerializer(serializers.ModelSerializer):
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
    
    commodity = CommoditySerializer(many=True,read_only=True)
    class Meta:
        model = CommodityCategory
        fields = '__all__'
        
class SuperVisorSampleFormWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperVisorSampleForm
        fields = '__all__'
    
    def validate(self, attrs):
        sample_form = attrs.get('sample_form')
        supervisor_user = attrs.get('supervisor_user')
        parameters = attrs.get('parameters')

        action = self.context['view'].action
        
        if len(attrs) == 3 and action == 'partial_update' and 'is_supervisor_sent' in attrs and 'status' in attrs and 'remarks' in attrs:
            if attrs.get('is_supervisor_sent') == True:
                id=self.context['view'].kwargs.get('pk')
                remarks  = attrs.get('remarks')
                UpdategenerateRawData(id,remarks) #  if sent to supervisor then generate logs
                return attrs
        elif action == 'partial_update':
            raise serializers.ValidationError('Partial updates not allowed....')
        if action == "create" and len(parameters)>1:
            for param in parameters:
                
                if SuperVisorSampleForm.objects.filter(sample_form=sample_form, parameters=param).exists():
                    raise serializers.ValidationError('A SuperVisorSampleForm with the same sample_form and parameter already exists(create)')
        elif action == "create" and len(parameters) == 1:
            for param in parameters:
                
                if SuperVisorSampleForm.objects.filter(sample_form=sample_form, parameters=param).exists():
                    sample_form_has_parameters_check = SampleFormHasParameter.objects.filter(sample_form = sample_form, parameter = param).exists()
                    if sample_form_has_parameters_check == False:
                        #print("False mk")
                        attrs['re_assign'] = True 
                    else:                         
                        #print("True mk")
                        raise serializers.ValidationError('You can not re-assign.')
            
        
        elif action == 'update' or action == 'partial_update':            
            instance_id = self.instance.id 
        
            sample_form_has_parameter_obj = SuperVisorSampleForm.objects.get(id=instance_id)  

            if SuperVisorSampleForm.objects.filter(sample_form=sample_form, supervisor_user=supervisor_user).exists() and sample_form_has_parameter_obj.sample_form == sample_form:
                pass

            else:
                raise serializers.ValidationError('A SuperVisorSampleForm with the same sample_form and analyst already exists(update)')
            
            for param in parameters:
                if sample_form_has_parameter_obj.parameters.filter(id=param.id).exists() and sample_form_has_parameter_obj.sample_form == sample_form: #if try to update same parameter as previous stored then dod nothing
                    pass
                elif SuperVisorSampleForm.objects.filter(sample_form=sample_form, parameters=param).exists(): #if try to update and not same as previous parameter then check already exist parameter.if exist then raise error
                    raise serializers.ValidationError('A SuperVisorSampleForm with the same sample_form and parameter already exists(update)')
                
        return attrs
    
    def create(self, validated_data):
            
        sample_form = validated_data['sample_form']
        supervisor_user = validated_data['supervisor_user']
        parameters = validated_data['parameters']
        test_type = validated_data['test_type']
        
        re_assign = validated_data.get('re_assign', False)    

        if re_assign == True:
            
            obj = SuperVisorSampleForm.objects.filter(sample_form=sample_form, parameters=parameters[0]).first()
                 
            if len(obj.parameters.all())>1:
                
                obj.parameters.remove(*parameters) #revoke parameter from existence obj
                obj.is_supervisor_sent = False
                # AlterRawDataStatus(obj)  # supervisor doesnot need alter status
                obj.save()

                # flushsupervisorprameterCalculate(obj,parameters) # supervisor doesnot need flush analyst data

                instance = SuperVisorSampleForm.objects.filter(sample_form=sample_form, supervisor_user=supervisor_user)
    
                if instance.exists():
                    instance = instance.first()
                    #AlterRawDataStatus(instance)
                    instance.parameters.add(*parameters) #if particular supervisor already exist then add parameter to that analysts re-asign
                    instance.is_supervisor_sent = False
                  
                    return instance
                else:
                    samp = SuperVisorSampleForm.objects.create(supervisor_user=supervisor_user,status="processing",sample_form_id=obj.sample_form_id,test_type = test_type)
                    samp.parameters.set(parameters)
                    samp.save()
                    
                    return obj
            else:
                if obj.supervisor_user == supervisor_user:
                    return obj
                else:
                    # raise serializers.ValidationError('remove from and re-assigning. i am fixing right now')
                    instance = SuperVisorSampleForm.objects.filter(sample_form=sample_form, supervisor_user=supervisor_user)
                    if instance.exists():
                        #print("exists")
                        instance = instance.first()
                        #AlterRawDataStatus(instance.first())
                        instance.parameters.add(*parameters) #if particular analysts already exist then add parameter to that analysts re-asign
                        instance.supervisor_user = supervisor_user
                        instance.save()
                        obj.delete()
                        return instance
                    elif obj.parameters.all().first() == parameters[0]:
                        obj.supervisor_user = supervisor_user
                        obj.parameters.add(*parameters)
                        obj.save()
                        return obj
                    else:
                        raise serializers.ValidationError('undefined assign supervisor rule')
                    
                    return obj
            # raise serializers.ValidationError('remove from and re-assigning. i am fixing right now')

        eventOnSampleform(sample_form,parameters)
        if SuperVisorSampleForm.objects.filter(sample_form=sample_form, supervisor_user=supervisor_user).exists():
            #print("testing ok append parameter")
            instance = SuperVisorSampleForm.objects.get(sample_form=sample_form, supervisor_user=supervisor_user)
            # Append the new parameters to the existing instance
            instance.parameters.add(*parameters)
            return instance
        
        return super().create(validated_data)


    
   
class SuperVisorSampleFormReadSerializer(serializers.ModelSerializer):  
    sample_form = SampleFormReadAnalystSerializer(read_only=True)
    commodity = CommodityWriteSerializer(read_only=True,many=True)
    parameters = TestResultLimitedSerializer(many=True,read_only=True)
    class Meta:
        model = SuperVisorSampleForm
        fields = '__all__'
       
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        sample_form_id = instance.sample_form.id
        # print(sample_form_id,"sasdadada sdd ds")
        # sample_form_id = generateDecodeIdforSampleForm(sample_form_id,self.context['request'].user)

        parameters_data = representation.get('parameters', [])

        assigned = 0
        for parameter_data in parameters_data:
            parameter_id = parameter_data.get('id')
            # Check if the parameter exists in SampleFormHasParameter model
            smple_frm_exist = SampleFormHasParameter.objects.filter(parameter=parameter_id, sample_form = sample_form_id)
            exists = smple_frm_exist.exists()

            if exists:
                analyst_obj = smple_frm_exist.first().analyst_user
                first_name = analyst_obj.first_name
                last_name = analyst_obj.last_name
                status = smple_frm_exist.first().status
                created_date = smple_frm_exist.first().created_date
                parameter_data['first_name'] = first_name
                parameter_data['last_name'] = last_name
                parameter_data['sample_form_has_parameter'] = smple_frm_exist.first().id
                parameter_data['assigned_date'] = created_date
                parameter_data['completed_date'] = smple_frm_exist.first().completed_date
                parameter_data['started_date'] = smple_frm_exist.first().started_date
                
                formula_obj_result = SampleFormParameterFormulaCalculate.objects.filter(sample_form_id=sample_form_id,parameter_id = parameter_id)
                if formula_obj_result.count()>0:
                    parameter_data['status'] = over_all_status[formula_obj_result.first().status]
                    
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
                    parameter_data['status'] = over_all_status['processing']
                    parameter_data['result'] = '-'

            parameter_data['exist'] = exists

            smple_frm_exist_for_supervisor = SuperVisorSampleForm.objects.filter(parameters=parameter_id, sample_form = sample_form_id)
            exists_supervisor_parameter = smple_frm_exist_for_supervisor.exists()
            parameter_data['exists_supervisor_parameter'] = exists_supervisor_parameter

            if exists_supervisor_parameter:
                # print(smple_frm_exist.first().analyst_user.username)
                try:
                    parameter_data['status_supervisor'] = "assigned"
                    parameter_data['supervisor_user'] = smple_frm_exist_for_supervisor.first().supervisor_user.username
                except:
                    pass 

            # if exists:
            #     # print(smple_frm_exist.first().analyst_user.username)
            #     try:
            #         parameter_data['status'] = smple_frm_exist.first().status
            #         if smple_frm_exist.first().status == "not_verified":
            #             parameter_data['status'] = over_all_status['completed']
            #         parameter_data['analyst'] = smple_frm_exist.first().analyst_user.username
            #     except:
            #         pass           


            if exists == True:
                assigned+=1

        representation['total_assign'] = assigned
        representation['parameters'] = parameters_data
        
        status = representation.get('status')
        request = self.context.get('request')

        if request.user.role == roles.USER:
            if status == "pending" or status == "processing" or status=="completed":
                representation['status'] = over_all_status[status]
            else:
                representation['status'] = over_all_status['processing']
                
        if request.user.role == roles.SUPERVISOR:
            representation['status'] = over_all_status[status]


        return representation
        

class SampleFormHasParameterReadSerializer(serializers.ModelSerializer):
    sample_form = SampleFormReadAnalystSerializer(read_only=True)
    commodity = CommodityAllReadSerializer(read_only=True)
    parameter = TestResultSerializer(many=True,read_only=True)
    assigned_by = serializers.SerializerMethodField()
    class Meta:
        model = SampleFormHasParameter
        fields = '__all__' 

    def get_assigned_by(self, obj):
        supervisor_table_obj = obj.super_visor_sample_form
        try:
            user = CustomUser.objects.get(id=supervisor_table_obj.supervisor_user.id)
            return ApprovedBySerializer(user).data
        except CustomUser.DoesNotExist:
            return None

    def get_parameter(self, obj):
        parameter_data = TestResultSerializer(obj.parameter, many=True).data
  
        count_status = 0
        for parameter in parameter_data:
            formula_calculate = SampleFormParameterFormulaCalculate.objects.filter(parameter = parameter['id'],sample_form=obj.sample_form_id).first()
            if formula_calculate:
                parameter['result'] = formula_calculate.result               
                count_status = count_status + 1   
                parameter['input_fields_value'] = formula_calculate.input_fields_value
                parameter['status'] = formula_calculate.status
                parameter['remarks'] = formula_calculate.remarks
                parameter['analyst_remarks'] = formula_calculate.analyst_remarks
                parameter['converted_result'] = formula_calculate.converted_result
                parameter['is_locked'] = formula_calculate.is_locked

                parameter['units_selected'] = formula_calculate.units
                parameter['mandatory_standard_selected'] = formula_calculate.mandatory_standard
                parameter['test_method_selected'] = formula_calculate.test_method
                parameter['additional_info'] = formula_calculate.additional_info
                
            else:
                parameter['result'] = ""     
             
            micro_table = MicroParameter.objects.filter(parameter = parameter['id'],sample_form=obj.sample_form_id,sample_form_has_parameter = obj.id,is_original = True)
            if micro_table.exists():
                parameter['micro_table'] = micro_table.last().id
            else:
                parameter['micro_table'] = None
         
        analyst_status = "processing"
        completed_done = 0
        recheck = False
        for parameter in parameter_data:
            formula_calculate = SampleFormParameterFormulaCalculate.objects.filter(parameter = parameter['id'],sample_form=obj.sample_form_id)
            if formula_calculate.exists():
                if formula_calculate.first().result != None:
                    if formula_calculate.first().status == "recheck":
                        recheck = True                
                    analyst_status = "completed"   
                    completed_done = completed_done + 1
                else:
                    analyst_status = "tested"
                    break
            else:                
                analyst_status = "processing" 
                break     
                
        total_len = len(parameter_data)
        if completed_done == 0:
            completed_done = str(total_len)
        elif completed_done == total_len:
            completed_done = ''
        else:
            try:
                completed_done = str(completed_done) + "/" +str(total_len)                
            except:
                completed_done = str(total_len)+"/"+str(completed_done)
                
        

        if count_status == 0:
            analyst_status = "pending"      
        elif recheck == True:
            completed_done = ''
            analyst_status = "recheck" 
       
            
        return parameter_data,analyst_status,completed_done
 
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(instance.parameter.first().id)
        parameter,analyst_status,total_completed = self.get_parameter(instance)
        representation['parameter'] = parameter

        if analyst_status == "completed" and instance.is_supervisor_sent == True:
            representation['status'] = over_all_status[instance.status]
        else:
            representation['status'] = analyst_status
        representation['completed_done'] = total_completed
        representation['completed_done'] = total_completed
        # representation['assigned_by'] = self.assigned_by

        return representation

class SampleFormHasParameterWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleFormHasParameter
        fields = '__all__' 

    def to_internal_value(self, data):
        if 'sample_form' in data:
            sample_form_id = data['sample_form'] 
            decoded_sample_form_id = generateDecodeIdforSampleForm(sample_form_id,self.context['request'].user)#smart_text(urlsafe_base64_decode(data['sample_form']))
            data['sample_form'] = decoded_sample_form_id
        return super().to_internal_value(data)
    
    def validate(self, attrs):
  
        check_verifier = SampleFormVerifier.objects.filter(sample_form_id = attrs.get('sample_form')).exists()
        if check_verifier:
            raise serializers.ValidationError('Sample Form already reached to Verifier so you can not modified')
        
        sample_form = attrs.get('sample_form')
        super_visor_sample_form_table = attrs.get('super_visor_sample_form')
        analyst_user = attrs.get('analyst_user')
        parameter = attrs.get('parameter')

        action = self.context['view'].action
        
        check_exist_for_other_supervisor = SampleFormHasParameter.objects.filter(sample_form = sample_form,analyst_user = analyst_user)

        if check_exist_for_other_supervisor.exists():
            obj_check_exist_for_other_supervisor = check_exist_for_other_supervisor.first()
            if obj_check_exist_for_other_supervisor.super_visor_sample_form.id != super_visor_sample_form_table.id:
                # print(obj_check_exist_for_other_supervisor.super_visor_sample_form,"::",super_visor_sample_form_table , "you are trying to update where other supervisor already assigned")
                raise serializers.ValidationError('you are trying to assign sample to analyst who is already assigned by other supervisor.')

        if len(attrs) == 3 and action == 'partial_update' and 'is_supervisor_sent' in attrs and 'status' in attrs and 'remarks' in attrs:
            if attrs.get('is_supervisor_sent') == True:
                id=self.context['view'].kwargs.get('pk')
                remarks  = attrs.get('remarks')

                completed_date =   timezone.now() #if analyst generate raw data sheet then add completed date
                attrs['completed_date'] = completed_date
                # raise serializers.ValidationError(' checking completed on date.',completed_date)

                
                generateRawData(id,remarks,completed_date) #  if sent to supervisor then generate logs
                # raise serializers.ValidationError('Fixing micro raw data ...')
                return attrs
        
        elif len(attrs) == 4 and action == 'partial_update' and 'started_date' in attrs and 'sample_received_date' in attrs and 'additional_info' in attrs and 'sample_receipt_condition' in attrs:
            return attrs
            
        elif action == 'partial_update':
            raise serializers.ValidationError('Partial updates not allowed....')
  
        if action == "create" and len(parameter)>1:
            for param in parameter:
                
                if SampleFormHasParameter.objects.filter(sample_form=sample_form, parameter=param).exists():
                    raise serializers.ValidationError('A SampleFormHasParameter with the same sample_form and parameter already exists(create)')
        elif action == "create" and len(parameter) == 1:
            for param in parameter:
                if SampleFormHasParameter.objects.filter(sample_form=sample_form, parameter=param).exists():
                    attrs['re_assign'] = True                          
            
          
        elif action == 'update' or action == 'partial_update':            
            instance_id = self.instance.id 
           
            sample_form_has_parameter_obj = SampleFormHasParameter.objects.get(id=instance_id)  

            if SampleFormHasParameter.objects.filter(sample_form=sample_form, analyst_user=analyst_user).exists() and sample_form_has_parameter_obj.sample_form == sample_form:
                pass

            else:
                raise serializers.ValidationError('A SampleFormHasParameter with the same sample_form and analyst already exists(update)')
            
            for param in parameter:
                if sample_form_has_parameter_obj.parameter.filter(id=param.id).exists() and sample_form_has_parameter_obj.sample_form == sample_form: #if try to update same parameter as previous stored then dod nothing
                    pass
                elif SampleFormHasParameter.objects.filter(sample_form=sample_form, parameter=param).exists(): #if try to update and not same as previous parameter then check already exist parameter.if exist then raise error
                    raise serializers.ValidationError('A SampleFormHasParameter with the same sample_form and parameter already exists(update)')
                   
        return attrs
    
    def create(self, validated_data):
        #print(" create tes md f")
       
        sample_form = validated_data['sample_form']
        analyst_user = validated_data['analyst_user']
        parameter = validated_data['parameter']        
        re_assign = validated_data.get('re_assign', False)    
        
        if re_assign == True:
            
            obj = SampleFormHasParameter.objects.filter(sample_form=sample_form, parameter=parameter[0]).first()
            
            if len(obj.parameter.all())>1:
                obj.parameter.remove(*parameter) #revoke parameter from existence obj
                obj.is_supervisor_sent = False
                AlterRawDataStatus(obj)
                obj.save()

                
                flushFormulaCalculate(obj,parameter)
            

                instance = SampleFormHasParameter.objects.filter(sample_form=sample_form, analyst_user=analyst_user)
                print(instance, " sdasd")
                if instance.exists():
                    print(2)
                    instance = instance.first()
                    AlterRawDataStatus(instance)
                    instance.parameter.add(*parameter) #if particular analysts already exist then add parameter to that analysts re-asign
                    instance.is_supervisor_sent = False
                  
                    return instance
                else:
                    print(analyst_user,obj.sample_form_id,obj.commodity_id,parameter)
                    print(3)
                    samp = SampleFormHasParameter.objects.create(analyst_user=analyst_user,status="processing",commodity_id = obj.commodity_id,sample_form_id=obj.sample_form_id,form_available=obj.form_available,super_visor_sample_form = obj.super_visor_sample_form)
                    samp.parameter.set(parameter)
                    samp.save()
                    
                    return obj
            else:
                if obj.analyst_user == analyst_user:
                    print(4)
                    return obj
                else:
                    # raise serializers.ValidationError('remove from and re-assigning. i am fixing right now')
                    print(5)
                    instance = SampleFormHasParameter.objects.filter(sample_form=sample_form, analyst_user=analyst_user)
                    print(instance," ins md")
                    if instance.exists():
                        #print("exists")
                        instance = instance.first()
                        AlterRawDataStatus(instance)
                        instance.parameter.add(*parameter) #if particular analysts already exist then add parameter to that analysts re-asign
                        instance.is_supervisor_sent = False
                        instance.save()
                        
                        obj.delete()

                        return instance
                    else:
                        pass
                        # obj.analyst_user = analyst_user
                        # flushFormulaCalculate(obj,parameter)
                        # AlterRawDataStatus(obj)
                        # obj.save()
                        
                        #print("this sample form has parameter have single parameter and this is changable analyst and this parameter and changeble analyst is not exist, so this need to create new and then delete,or simply change analyst name")
                    
                    return obj
            # raise serializers.ValidationError('remove from and re-assigning. i am fixing right now')
        print(6)
        if SampleFormHasParameter.objects.filter(sample_form=sample_form, analyst_user=analyst_user).exists():
            #print("testing ok append parameter")
            instance = SampleFormHasParameter.objects.get(sample_form=sample_form, analyst_user=analyst_user)
            # Append the new parameters to the existing instance
            instance.parameter.add(*parameter)
            return instance
        
        return super().create(validated_data)

def flushFormulaCalculate(obj,parameter):
    formula_calculate_obj = obj.formula_calculate.all().filter(parameter_id = parameter[0])
    formula_calculate_obj.delete()
    # print(formula_calculate_obj)
    #print("flushing formula calculate")

def flushsupervisorprameterCalculate(obj,parameter):
    pass
    # formula_calculate_obj = obj.formula_calculate.all().filter(parameter_id = parameter[0])
    # formula_calculate_obj.delete()
    # print(formula_calculate_obj)
    #print("flushing formula calculate")


def AlterRawDataStatus(obj):
    raw_data_obj = obj.raw_datasheet.all().last()
    print(raw_data_obj," obj none")
    if raw_data_obj == None:
        pass
        #print("this sample form has parameter haave not raw data sheet")
    else:
        raw_data_obj.status = "re-assign"
        raw_data_obj.save()
    #print("alter raw data status")

def eventOnSampleform(sample_form_id,parameters):
    sample_form_obj = sample_form_id

    sample_obj_params = sample_form_obj.parameters.all().count()
    supervisor_params = 0
    supervisor_objss = SuperVisorSampleForm.objects.filter(sample_form = sample_form_obj.id)
    for supervisor_ob in supervisor_objss: # if all supervisor analyst_test is True then update in sample form is_analyst_test = True
        params = supervisor_ob.parameters.all().count()
        supervisor_params = supervisor_params + params
    supervisor_params = supervisor_params + len(parameters)
   
    if sample_obj_params != supervisor_params:
        statuss = "not_assigned"
        form_availables = "smu"
        SampleForm.objects.filter(id=sample_form_obj.id).update(is_analyst_test = False,status=statuss,form_available = form_availables)
    else:
        statuss = "processing"
        form_availables = "supervisor"
        SampleForm.objects.filter(id=sample_form_obj.id).update(is_analyst_test = False,status=statuss,form_available = form_availables)

class NoticeImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeImages
        fields = '__all__'


class ApprovedListSerializer(serializers.ModelSerializer):
    user = ApprovedByListSerializer(read_only = True)
    class Meta:
        model = ApprovedList
        fields = '__all__'

class ApprovedWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovedList
        fields = '__all__'


class VerifiedListSerializer(serializers.ModelSerializer):
    user = ApprovedByListSerializer(read_only = True)
    class Meta:
        model = VerifiedList
        fields = '__all__'

class VerifiedWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifiedList
        fields = '__all__'