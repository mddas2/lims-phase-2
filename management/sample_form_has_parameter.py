from django.shortcuts import render,redirect
from django.http import HttpResponse
from .serializers import SampleFormHasParameterReadSerializer,SampleFormHasParameterWriteSerializer
from .models import SampleFormHasParameter,TestResult
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .pagination import MyLimitOffsetPagination
from rest_framework.response import Response
from .custompermission import SampleFormHasParameterPermission
from rest_framework import status
from rest_framework.filters import OrderingFilter,SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from . import roles
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q

class SampleFormHasParameterViewSet(viewsets.ModelViewSet):
    queryset = SampleFormHasParameter.objects.all()
    serializer_class = SampleFormHasParameterReadSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['status','sample_form__name','sample_form__id','sample_form__code','sample_form__namuna_code','sample_form__refrence_number','sample_form__sample_lab_id']
    filterset_fields = ['status','form_available','analyst_user','sample_form','commodity','']

    filterset_fields = {
        'sample_form__name': ['exact', 'icontains'],
        'sample_form__owner_user': ['exact'],
        'sample_form__status': ['exact'],
        'sample_form__form_available': ['exact'],
        'sample_form__commodity_id': ['exact'],
        'sample_form__supervisor_user': ['exact'],
        'analyst_user':['exact'],
        'sample_form__commodity':['exact'],
        'created_date': ['date__gte', 'date__lte']  # Date filtering
    }

    ordering_fields = ['id']
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,SampleFormHasParameterPermission]
    pagination_class = MyLimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        
        if user.role == roles.ANALYST:
            return SampleFormHasParameter.objects.filter(analyst_user = user).filter(~Q(status='verified')).filter(~Q(status='rejected')).order_by("-created_date")       
        else:
             raise PermissionDenied("You do not have permission to access this resource.")

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SampleFormHasParameterWriteSerializer
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        supervisor_obj = serializer.validated_data['super_visor_sample_form']
        supervisor_parameters = supervisor_obj.parameters.all()

        all_assigned_parameters = TestResult.objects.filter(sample_has_parameters__super_visor_sample_form_id=supervisor_obj.id) #is supervisor has assigned 

        if supervisor_parameters.count() == all_assigned_parameters.count():
            total_assiged = True
        else:
            total_assiged = False

        # Create a custom response
        response_data = {
            "message": "created successfully",
            "data": serializer.data,
            "total_assigned" : total_assiged
        }

        # Return the custom response
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Save the updated object to the database
        self.perform_update(serializer)

        # Create a custom response
        response_data = {
            "message": "updated successfully",
            "data": serializer.data
        }

        # Return the custom response
        return Response(response_data)