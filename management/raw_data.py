from .models import RawDataSheet,RawDataSheetDetail,TestResult,SampleFormHasParameter
from django.db.models import Q
from management import roles
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .raw_data_serializer import rawDataSerializer,rawDataTestTypeSerializer,rawDataTestTypeGlobalSerializer
from . encode_decode import generateDecodeIdforSampleForm
from django.http import HttpResponse
from management.models import MicroParameter
from rest_framework import serializers
from .models  import MicroParameterRawData,MicroObservationTableRawData
from rest_framework.response import Response

def generateRawData(sample_form_has_parameter_id,remarks,completed_date):
    
    obj = SampleFormHasParameter.objects.get(id=sample_form_has_parameter_id)
   
    formula_calculate_parameters = obj.formula_calculate.all()

    sample_form_id = obj.sample_form.id
    supervisor_remarks = obj.sample_form.remarks

    super_visor_sample_form_id = obj.super_visor_sample_form.id

    test_type2 = obj.parameter.all().first().test_type

   
    if obj.completed_date == None:
        completed_date = completed_date
    else:
        completed_date  = obj.completed_date

    raw_data_sheet_instance = RawDataSheet(super_visor_sample_form_id = super_visor_sample_form_id ,sample_form_id=sample_form_id,sample_form_has_parameter_id = obj.id,remarks=remarks,status="not_verified",analyst_user=obj.analyst_user,supervisor_remarks=supervisor_remarks,test_type = test_type2,started_date = obj.started_date,completed_date=completed_date,sample_received_date = obj.sample_received_date,additional_info=obj.additional_info,sample_receipt_condition = obj.sample_receipt_condition)
    raw_data_sheet_instance.save()
    
   
    for param in formula_calculate_parameters:
        test_type = param.parameter.test_type

        if test_type == "Microbiological":
            micro_table = MicroParameter.objects.filter(parameter = param.parameter_id,sample_form=sample_form_id,sample_form_has_parameter = obj.id,is_original = True).last()
            generate_micro_raw_data = generateMicroRawData(micro_table)
            
            # print(micro_table," micro table")
            data = {
                'raw_data_id':raw_data_sheet_instance.id,
                'parameter_id':param.parameter.id,
                'result':param.result,
                'is_verified':param.is_verified,
                'input_fields_value':param.input_fields_value,
                'auto_calculate_result':param.auto_calculate_result,
                'remark':param.remarks,
                'micro_table_id' : generate_micro_raw_data,

                'converted_result':param.converted_result,
                'analyst_remarks':param.analyst_remarks,
                'decimal_place':param.decimal_place,

                 "units":param.units,
                 "mandatory_standard":param.mandatory_standard,
                 "test_method":param.test_method,
                 "additional_info":param.additional_info,

            }
        else:
            data = {
                'raw_data_id':raw_data_sheet_instance.id,
                'parameter_id':param.parameter.id,
                'result':param.result,
                'is_verified':param.is_verified,
                'input_fields_value':param.input_fields_value,
                'auto_calculate_result':param.auto_calculate_result,
                'remark':param.remarks,

                'converted_result':param.converted_result,
                'analyst_remarks':param.analyst_remarks,
                'decimal_place':param.decimal_place,

                "units":param.units,
                "mandatory_standard":param.mandatory_standard,
                "test_method":param.test_method,
                "additional_info":param.additional_info,
                
            }
        RawDataSheetDetail.objects.update_or_create(**data)
    return True

class MicroParameterRawDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroParameterRawData
        fields = '__all__'

class MicroObservationTableRawDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroObservationTableRawData
        fields = '__all__'


def generateMicroRawData(micro_table):

    micro_table_raw_data_serializer_data = MicroParameterRawDataSerializer(micro_table)
    micro_table_raw_data_serializer = MicroParameterRawDataSerializer(data=micro_table_raw_data_serializer_data.data)

    if micro_table_raw_data_serializer.is_valid():
        micro_raw_data_saved_obj = micro_table_raw_data_serializer.save()
        pass
        # print(micro_table_raw_data_serializer.data, "serializer")
    else:
        #print("not valid")
        return HttpResponse("not valid...")

    micro_observation_table = micro_table.micro_observation_table.all()
    for micro_observation in micro_observation_table:
        micro_observation_table_raw_data_serializer_get = MicroObservationTableRawDataSerializer(micro_observation)
        data_to_save = micro_observation_table_raw_data_serializer_get.data
        data_to_save['micro_parameter_table_raw_data'] = micro_raw_data_saved_obj.id  # Corrected this line
        #print("\n\n",micro_raw_data_saved_obj.id)
        micro_observation_table_raw_data_serializer_save = MicroObservationTableRawDataSerializer(data=data_to_save)
        if micro_observation_table_raw_data_serializer_save.is_valid():
            micro_observation_table_raw_data_serializer_save.save()
        else:
            pass
            # print(micro_observation_table_raw_data_serializer_save.errors)

    return micro_raw_data_saved_obj.id



    # for item in micro_table_raw_data_serializer.data:
    #     destination_data.append({
    #         'field1': item['field1'],
    #         'field2': item['field2'],
    #     })
    
    # destination_serializer = DestinationModelSerializer(data=destination_data, many=True)
    # if destination_serializer.is_valid():
    #     destination_serializer.save()
    #     return Response({'message': 'Data copied successfully'}, status=status.HTTP_201_CREATED)
    # else:
    #     return Response(destination_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def UpdategenerateRawData(supervisor_table_id,remarks):
   raw_data_sheet_supervisor =  RawDataSheet.objects.filter(super_visor_sample_form_id = supervisor_table_id)
   raw_data_sheet_supervisor.update(supervisor_remarks = remarks)
   #print("remarks added to supervisor")
   


class rawDataDetail(generics.ListAPIView):
    # queryset = SampleForm.objects.all() 
    # serializer_class = CompletedSampleFormHasAnalystSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
  
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']


    def get_queryset(self):

        sample_form_has_parameter_id = self.kwargs.get('sample_form_has_parameter')
        query = RawDataSheet.objects.filter(sample_form_has_parameter_id=sample_form_has_parameter_id)
    
        return query
    
    def get_serializer_class(self):
        serializer = rawDataSerializer
        return serializer
        
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class rawDataForSampleForm(generics.ListAPIView):
    # queryset = SampleForm.objects.all() 
    # serializer_class = CompletedSampleFormHasAnalystSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
  
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']


    def get_queryset(self):

        sample_form_id = self.kwargs.get('sample_form')
        user = self.request.user
        sample_form_id = generateDecodeIdforSampleForm(sample_form_id,user) 
        query = RawDataSheet.objects.filter(sample_form_id=sample_form_id)
    
        return query
    
    def get_serializer_class(self):
        serializer = rawDataSerializer
        return serializer
        
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class rawDataForSampleFormTestType(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
  
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    def get_queryset(self):
        sample_form_id = self.kwargs.get('sample_form')
        user = self.request.user
        sample_form_id = generateDecodeIdforSampleForm(sample_form_id, user)
        query = RawDataSheet.objects.filter(sample_form_id=sample_form_id, super_visor_sample_form__supervisor_user=user.id)
        return query
    
    def get_serializer_class(self):
        return rawDataTestTypeSerializer
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        test_type_data = {}
        for item in data:
            test_type = item.pop('test_type')
            if test_type not in test_type_data:
                test_type_data[test_type] = []
            test_type_data[test_type].append(item)

        response = {}
        for test_type, test_type_values in test_type_data.items():
            response[test_type] = test_type_values

        return Response(response)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    
class rawDataForSampleFormGlobal(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
  
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    def get_queryset(self):
        sample_form_id = self.kwargs.get('sample_form')
        user = self.request.user
        sample_form_id = generateDecodeIdforSampleForm(sample_form_id, user)
        query = RawDataSheet.objects.filter(sample_form_id=sample_form_id)#.filter(Q(status = "not_approved") status= "not_verified") blunder fix
        return query
    
    def get_serializer_class(self):
        return rawDataTestTypeGlobalSerializer
        
    def list(self, request, *args, **kwargs):
        from rest_framework.response import Response
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        test_type_data = {}
        for item in data:
            test_type = item.pop('test_type')
            if test_type not in test_type_data:
                test_type_data[test_type] = []
            test_type_data[test_type].append(item)

        response = {}
        for test_type, test_type_values in test_type_data.items():
            response[test_type] = test_type_values

        return Response(response)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)