from django.shortcuts import render,redirect
from django.http import HttpResponse
from .serializers import FiscalYearSerializer,limitedCommidityCategoryreadSerializer,limitedCommidityreadSerializer,TestResultWriteSerializer,MicroObservationTableSerializer,MicroParameterSerializer,ClientCategorySerializer, SampleFormWriteSerializer,SampleFormReadSerializer, CommoditySerializer, CommodityCategorySerializer, TestResultSerializer,PaymentSerializer,SuperVisorSampleFormReadSerializer,SuperVisorSampleFormWriteSerializer,NoticeImagesSerializer,ApprovedListSerializer,VerifiedListSerializer,VerifiedWriteSerializer,ApprovedWriteSerializer
from .models import FiscalYear,ClientCategory,Units,MandatoryStandard,TestMethod, SampleForm, Commodity, CommodityCategory,TestResult, Payment,SuperVisorSampleForm,MicroParameter,MicroObservationTable,ClientCategoryDetail , NoticeImages , ApprovedList , VerifiedList
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .pagination import MyLimitOffsetPagination
from rest_framework.response import Response
from . client_category_serializers import ClientCategoryDetailSerializer,ClientCategoryDetailImagesSerializer
from .custompermission import FiscalYearPermission,ClientCategoryPermission,SampleFormViewSetPermission,CommodityViewSetPermission,CommodityCategoryViewSetPermission,TestResultViewSetPermission,PaymentViewSetPermission,MicroparameterViewsetPermission,SuperVisorSampleFormViewsetPermission,NoticeImagesPermission,ApprovedListPermission,VerifiedListPermission
from rest_framework import status
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from . import roles
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from . encode_decode import generateDecodeIdforSampleForm
from rest_framework import generics
from django.core.cache import cache
cache_time = 300 # 300 is 5 minute

class ClientCategoryViewSet(viewsets.ModelViewSet):
    queryset = ClientCategory.objects.all()
    serializer_class = ClientCategorySerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name','id']
    permission_classes = [ClientCategoryPermission]
    pagination_class = MyLimitOffsetPagination
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "client category created successfully",
            "data": serializer.data
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
            "message": "client category updated successfully",
            "data": serializer.data
        }

        # Return the custom response
        return Response(response_data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Perform the default delete logic
        self.perform_destroy(instance)

        # Create a custom response
        response_data = {
            "message": "client category deleted successfully"
        }

        # Return the custom response
        return Response(response_data)

class SuperVisorSampleFormViewset(viewsets.ModelViewSet):
    queryset = SuperVisorSampleForm.objects.all()
    serializer_class = SuperVisorSampleFormReadSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']
    filterset_fields = {
        'supervisor_user': ['exact'],
        'status': ['exact'],       
        'created_date': ['date__gte', 'date__lte']  # Date filtering
    }
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,SuperVisorSampleFormViewsetPermission]
    pagination_class = MyLimitOffsetPagination


    def get_queryset(self):
        user = self.request.user
        action = self.action

        if action == 'list':
            query = SuperVisorSampleForm.objects.filter(supervisor_user=user.id,status = "not_assigned")
        elif action == 'retrieve':
            query = SuperVisorSampleForm.objects.filter(supervisor_user=user.id)
        else:
            query = SuperVisorSampleForm.objects.filter(supervisor_user=user.id)

        if user.role != roles.SUPERVISOR:
            raise PermissionDenied("You do not have permission to access thais resource.")
        
        return query.order_by("-created_date")
        
        
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SuperVisorSampleFormWriteSerializer
        return super().get_serializer_class()
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
    
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        
        # Add extra response data for retrieve action
        extra_data = {
            "extra_field": "Extra value for retrieve",
            "another_field": "Another value for retrieve"
        }
        # response.data.update(extra_data)
        return response
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # this is for redirect for angular
        created_data = serializer.data

        sample_form_id = created_data['sample_form']
        sample_form_obj = SampleForm.objects.get(id=sample_form_id)
        all_parameters = sample_form_obj.parameters.all()

        all_supervisor_parameters = TestResult.objects.filter(supervisor_has_parameter__sample_form_id=sample_form_id)

        if all_parameters.count() == all_supervisor_parameters.count():
            total_assiged = True
        else:
            total_assiged = False

        # print(all_parameters.count(),"::",all_supervisor_parameters.count())
        # Create a custom response
        response_data = {
            "message": "submitted successfully",
            "data": serializer.data,
            "total_assiged" : total_assiged
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

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Save the updated object to the database
        self.perform_update(serializer)

        # Create a custom response
        response_data = {
            "message": "partially updated successfully",
            "data": serializer.data
        }

        # Return the custom response
        return Response(response_data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Perform the default delete logic
        self.perform_destroy(instance)

        # Create a custom response
        response_data = {
            "message": "deleted successfully"
        }

        # Return the custom response
        return Response(response_data)
    
class SampleFormViewSet(viewsets.ModelViewSet):
    queryset = SampleForm.objects.all()
    serializer_class = SampleFormReadSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','name','owner_user','status','form_available','commodity__name','refrence_number','sample_lab_id']
    ordering_fields = ['name','id']
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'owner_user': ['exact'],
        'status': ['exact'],
        'form_available': ['exact'],
        'commodity_id': ['exact'],
        'supervisor_user': ['exact'],
        'created_date': ['date__gte', 'date__lte'],  # Date filtering
        'client_category_detail__client_category':['exact'],
    }
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,SampleFormViewSetPermission]
    pagination_class = MyLimitOffsetPagination

    def get_object(self):
        user = self.request.user

        id = generateDecodeIdforSampleForm(self.kwargs['pk'],user) 
    
        queryset = self.get_queryset()
        obj = queryset.filter(id=id).first()
        if not obj:
            raise Http404("Object not found")

        return obj

    def get_queryset(self):
        user = self.request.user

        if user.role == roles.USER:         
            # query =  SampleForm.objects.filter(Q(owner_user = user.email) & ~Q(status="completed") & ~Q(status="rejected") )
            query =  SampleForm.objects.filter(Q(owner_user = user.email)).filter(~Q(status="completed")).filter(~Q(status="rejected") )
        elif user.role == roles.SUPERVISOR:
            query =  SampleForm.objects.filter(supervisor_user=user,status="not_assigned")
            if self.request.method == "PATCH":
                query =  SampleForm.objects.filter(supervisor_user=user)
        elif user.role == roles.SMU:
            query = SampleForm.objects.filter(Q(form_available = 'smu') or Q(status = "not_assigned")).filter(~Q(status = "rejected")).filter(~Q(status = "recheck"))
        elif user.role == roles.SUPERADMIN:
            query = SampleForm.objects.filter(Q(form_available = 'smu') or Q(status = "not_assigned")).filter(~Q(status = "rejected"))
        elif user.role == roles.ADMIN:
            query = SampleForm.objects.filter(status = "not_approved")
        elif user.role == roles.VERIFIER:
            query = SampleForm.objects.filter(status = "not_verified")
        else:
            raise PermissionDenied("You do not have permission to access this resource.")
        
        return query.order_by("-created_date")
        
        
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SampleFormWriteSerializer
        return super().get_serializer_class()
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
    
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        
        # Add extra response data for retrieve action
    
        # response.data.update(extra_data)
        return response
    
    def create(self, request, *args, **kwargs):

        name = request.POST.getlist('images[name]')
        files =  request.FILES.getlist('images[file]')
        client_sub_category = request.data.get('client_sub_category')
     
        client_category = request.data.get('client_category')

        create_client,client_category_detail = CeateClientCategoryDetail(name,files,client_category,client_sub_category)
        
        if create_client:
            from django.http import QueryDict
            
            mutable_data = QueryDict(mutable=True)
            mutable_data.update(request.data)


            # Set the client_category_detail_id in the mutable data
            mutable_data['client_category_detail'] = client_category_detail

            serializer = self.get_serializer(data=mutable_data)
            if serializer.is_valid() == False:
                ClientCategoryDetail.objects.get(id = client_category_detail).delete()
            serializer.is_valid(raise_exception=True)

            # Save the new object to the database
            self.perform_create(serializer)

            # Create a custom response
            response_data = {
                "message": "Sample submitted successfully",
                "data": serializer.data
            }

            # Return the custom response
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            esponse_data = {
                "message": " can not create ",
            }

            # Return the custom response
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Save the updated object to the database
        self.perform_update(serializer)

        # Create a custom response
        response_data = {
            "message": "Sample updated successfully",
            "data": serializer.data
        }

        # Return the custom response
        return Response(response_data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Save the updated object to the database
        self.perform_update(serializer)
        # print(serializer.data)
        # Create a custom response
        response_data = {
            "message": "Sample partially updated successfully",
            "data": serializer.data
        }

        # Return the custom response
        return Response(response_data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Perform the default delete logic
        self.perform_destroy(instance)

        # Create a custom response
        response_data = {
            "message": "Sample deleted successfully"
        }

        # Return the custom response
        return Response(response_data)
    
    
class CommodityViewSet(viewsets.ModelViewSet):
    serializer_class = CommoditySerializer   

    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','name','test_result__name']
    ordering_fields = ['name','id','category__name']
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'category_id': ['exact'],
    }

    authentication_classes = [JWTAuthentication]
    permission_classes = [CommodityViewSetPermission]
    pagination_class = MyLimitOffsetPagination
    
    # def get_queryset(self):
    #     query = Commodity.objects.all()
    #     return query
    
    
    # def list(self, request, *args, **kwargs):
    #     # Try to get cached data
 
    #     cached_data = cache.get('CommodityViewSet')

    #     if cached_data is None:
    #         # Cache is empty, fetch data from the database
    #         queryset = self.filter_queryset(self.get_queryset())
            
    #         # Use pagination to get a page of data
    #         page = self.paginate_queryset(queryset)
    #         if page is not None:
    #             serializer = self.get_serializer(page, many=True)
    #             data = self.get_paginated_response(serializer.data).data
    #         else:
    #             data = []

    #         cache.set('CommodityViewSet', data, cache_time)
    #     else:
    #         data = cached_data
        
    #     return Response(data)
    
    def get_queryset(self):
        cached_data = cache.get('CommodityViewSet')
        if cached_data is None:
            query = Commodity.objects.all()
            cache.set('CommodityViewSet', query, cache_time)
        else:
            query = cached_data
        return query
    
    
    def list(self, request, *args, **kwargs):
        
        # Cache is empty, fetch data from the database
  
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data).data
        else:
            data = []       
        return Response(data)

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "commodity created successfully",
            "data": serializer.data
        }

        cache.delete('CommodityViewSet')
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
            "message": "commodity updated successfully",
            "data": serializer.data
        }

        # Return the custom response
        cache.delete('CommodityViewSet')
        return Response(response_data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Perform the default delete logic
        self.perform_destroy(instance)

        # Create a custom response
        response_data = {
            "message": "commodity deleted successfully"
        }

        # Return the custom response
        return Response(response_data)
    
class commodityLimitedData(generics.ListAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    filter_backends  = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']
    pagination_class = MyLimitOffsetPagination

    def get_queryset(self):
        commodity = Commodity.objects.all()
        return commodity

    def get_serializer_class(self):
        return limitedCommidityreadSerializer
        
    def list(self, request, *args, **kwargs):
        from rest_framework.response import Response
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        return Response(data)

class commodityCategoryLimitedData(generics.ListAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    filter_backends  = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    pagination_class = MyLimitOffsetPagination

    def get_queryset(self):
        commodity = CommodityCategory.objects.all()
        return commodity

    def get_serializer_class(self):
        return limitedCommidityCategoryreadSerializer
        
    def list(self, request, *args, **kwargs):
        # Try to get cached data
        cached_data = cache.get('commodityCategoryLimitedData')

        if cached_data is None:
            # Cache is empty, fetch data from the database
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

            # Store data in the cache for 5 minutes (300 seconds)
            cache.set('commodityCategoryLimitedData', data, cache_time)
        else:
            data = cached_data
        
        return Response(data)
    
class CommodityCategoryViewSet(viewsets.ModelViewSet):

    queryset = CommodityCategory.objects.all()
    serializer_class = CommodityCategorySerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    filterset_fields = ['name','id']
    search_fields = ['name']
    authentication_classes = [JWTAuthentication]
    permission_classes = [CommodityCategoryViewSetPermission]
    pagination_class = MyLimitOffsetPagination

    def list(self, request, *args, **kwargs):
        # Try to get cached data
        cached_data = cache.get('CommodityCategoryViewSet')

        if cached_data is None:
            # Cache is empty, fetch data from the database
            queryset = self.filter_queryset(self.get_queryset())
            
            # Use pagination to get a page of data
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = self.get_paginated_response(serializer.data).data
            else:
                data = []

            # Store data in the cache for 5 minutes (300 seconds)
            cache.set('CommodityCategoryViewSet', data, cache_time)
        else:
            data = cached_data
        
        return Response(data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "commodity category created successfully",
            "data": serializer.data
        }

        # Return the custom response
        
        cache.delete("CommodityCategoryViewSet")
        cache.delete("commodityCategoryLimitedData")
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
            "message": "commodity category updated successfully",
            "data": serializer.data
        }

        # Return the custom response
        cache.delete("CommodityCategoryViewSet")
        cache.delete("commodityCategoryLimitedData")
        return Response(response_data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Perform the default delete logic
        self.perform_destroy(instance)

        # Create a custom response
        response_data = {
            "message": "commodity category deleted successfully"
        }

        # Return the custom response
        cache.delete("CommodityCategoryViewSet")
        cache.delete("commodityCategoryLimitedData")
        return Response(response_data)

class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id','name','formula','commodity__name']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,TestResultViewSetPermission]
    pagination_class = MyLimitOffsetPagination
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TestResultWriteSerializer
        return super().get_serializer_class()
    
    def list(self, request, *args, **kwargs):
        # Try to get cached data
        cached_data = cache.get('TestResultViewSet')

        if cached_data is None:
            # Cache is empty, fetch data from the database
            queryset = self.filter_queryset(self.get_queryset())
            
            # Use pagination to get a page of data
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = self.get_paginated_response(serializer.data).data
            else:
                data = []

            # Store data in the cache for 5 minutes (300 seconds)
            cache.set('TestResultViewSet', data, cache_time)
        else:
            data = cached_data
        
        return Response(data)
    
    def create(self, request, *args, **kwargs):
        units = request.data.get('units')
        data = additionalOperation(request.data)
        print(data," return data from function...")
        # return HttpResponse(data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "parameter created successfully",
            "data": serializer.data
        }

        # Return the custom response

        cache.delete("TestResultViewSet")
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        

        data = additionalOperation(request.data)
        
        serializer = self.get_serializer(data=request.data)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Save the updated object to the database
        self.perform_update(serializer)

        # Create a custom response
        response_data = {
            "message": "parameter updated successfully",
            "data": serializer.data
        }

        # Return the custom response
        cache.delete("TestResultViewSet")
        return Response(response_data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Perform the default delete logic
        self.perform_destroy(instance)

        # Create a custom response
        response_data = {
            "message": "parameter deleted successfully"
        }

        # Return the custom response
        cache.delete("TestResultViewSet")
        return Response(response_data)

class PaymentViewSet(viewsets.ModelViewSet):
    from rest_framework.parsers import MultiPartParser, FormParser
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,PaymentViewSetPermission]
    pagination_class = MyLimitOffsetPagination
    
    parser_classes = [MultiPartParser, FormParser]
    
    def create(self, request, *args, **kwargs):
        payment_dict = {}
        for key, value in request.data.items():
            if key.startswith('payments'):
                start_index = key.index('[')
                end_index = key.index(']')
                index = key[start_index + 1:end_index]
                field = key[end_index + 2:-1]  # Adjust the index according to the key format

                if index not in payment_dict:
                    payment_dict[index] = {}
               
                if value == "undefined" and field == "payment_receipt":
                   
                    pass
                else:
                    payment_dict[index][field] = value

        payment_data = []
   
        for index, payment_data_dict in payment_dict.items():
            serializer = PaymentSerializer(data=payment_data_dict)
            serializer.is_valid(raise_exception=True)
            payment_obj = serializer.save()
            payment_data.append(serializer.data)

        response_data = {
            "message": "Payments created successfully",
            "data": payment_data
        }

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
            "message": "payment updated successfully",
            "data": serializer.data
        }

        # Return the custom response
        return Response(response_data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Perform the default delete logic
        self.perform_destroy(instance)

        # Create a custom response
        response_data = {
            "message": "payment deleted successfully"
        }

        # Return the custom response
        return Response(response_data)

class MicroparameterViewset(viewsets.ModelViewSet):
    queryset = MicroParameter.objects.all()
    serializer_class = MicroParameterSerializer   
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    ordering_fields = ['id']
    search_fields = ['id']
    filterset_fields = ['id']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,MicroparameterViewsetPermission]
    pagination_class = MyLimitOffsetPagination
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "MicroparameterViewset created successfully",
            "data": serializer.data
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
            "message": "MicroparameterViewset updated successfully",
            "data": serializer.data
        }

        # Return the custom response
        return Response(response_data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Perform the default delete logic
        self.perform_destroy(instance)

        # Create a custom response
        response_data = {
            "message": "MicroparameterViewset deleted successfully"
        }

        # Return the custom response
        return Response(response_data)
    
class MicroObservationTableViewSet(viewsets.ModelViewSet):
    queryset = MicroObservationTable.objects.all()
    serializer_class = MicroObservationTableSerializer   
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    ordering_fields = ['id']
    search_fields = ['id']
    filterset_fields = ['id']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,MicroparameterViewsetPermission]
    pagination_class = MyLimitOffsetPagination
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,many=True)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "MicroObservationTable created successfully",
            "data": serializer.data
        }

        # Return the custom response
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        
        data = request.data
        
        response_data = {}
        for dat in data:
            partial = kwargs.pop('partial', False)
            instance = MicroObservationTable.objects.get(id = dat['id'])
            serializer = self.get_serializer(instance, data=dat, partial=partial)
            serializer.is_valid(raise_exception=True)

            # Save the updated object to the database
            self.perform_update(serializer)

        # Create a custom response
            response_data = {
                "message": "MicroObservationTable updated successfully",
                "data": serializer.data
            }

        # Return the custom response
        return Response(response_data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Perform the default delete logic
        self.perform_destroy(instance)

        # Create a custom response
        response_data = {
            "message": "MicroObservationTable deleted successfully"
        }

        # Return the custom response
        return Response(response_data)

    
def Home(request):
    from account.models import CustomUser
    from management.models import ClientCategory
    clien_category = ClientCategory.objects.get(id='1')
    user = CustomUser.objects.get(id='1')
    user.client_category = clien_category
    user.save()
    return HttpResponse(user)

def CeateClientCategoryDetail(names,files,client_category,client_sub_category):
    
    data = {
        'client_category':client_category,
        'client_sub_category':client_sub_category,
    }
    
    serializer = ClientCategoryDetailSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    image_data = []


    for name, file in zip(names, files):
       #print("name:",name," file:",file,int(serializer.data['id']))
       dict_data = {
                'client_category_detail':int(serializer.data['id']),
                'name':name,
                'file':file,
            }
       image_data.append(dict_data)

    image_serializer = ClientCategoryDetailImagesSerializer(many=True,data=image_data)
    if image_serializer.is_valid() == False:
        ClientCategoryDetail.objects.get(id = int(serializer.data['id'])).delete()

    image_serializer.is_valid(raise_exception=True)
    image_serializer.save()
    
    return True,int(serializer.data['id'])
   
def additionalOperation(data):
 
    units = data.get('units')
    ref_test_method = data.get('test_method')
    mandatory_standard = data.get('mandatory_standard')

    units = createOrUpdateUnits(units)
    ref_test_method = createOrUpdateRefTestMethod(ref_test_method)
    mandatory_standard = createOrUpdateMandatoryStandards(mandatory_standard)


  
    data['units'] = units
    data['test_method'] = ref_test_method
    data['mandatory_standard'] = mandatory_standard

    return data

def createOrUpdateUnits(units):
    units_ids = []
    for unit in units:
        unit_data = {
            'units_nepali':unit['units_nepali']
        }
        create_unit_obj,create = Units.objects.update_or_create(units = unit['units'],defaults=unit_data)
        # print(create_unit_obj,"::" , "created unit ")
        units_ids.append(create_unit_obj.id)

    return units_ids

def createOrUpdateRefTestMethod(test_methods):
    test_methods_ids = []
    for test_method in test_methods:
        # test_method_data = {
        #     'ref_test_method_nepali':test_method['ref_test_method_nepali']
        # }
        test_methods_obj,create = TestMethod.objects.update_or_create(ref_test_method = test_method['ref_test_method'],defaults=None)
        # print(create_unit_obj,"::" , "created unit ")
        test_methods_ids.append(test_methods_obj.id)

    return test_methods_ids
def createOrUpdateMandatoryStandards(mandatory_standards):
    mandatory_standards_ids = []
    for mandatory_standard in mandatory_standards:
        mandatory_standard_data = {
            'mandatory_standard_nepali':mandatory_standard['mandatory_standard_nepali']
        }
        mandatory_standards_obj,create = MandatoryStandard.objects.update_or_create(mandatory_standard = mandatory_standard['mandatory_standard'],defaults=mandatory_standard_data)
        # print(create_unit_obj,"::" , "created unit ")
        mandatory_standards_ids.append(mandatory_standards_obj.id)

    return mandatory_standards_ids
             
class FiscalyearViewSet(viewsets.ModelViewSet):
    queryset = FiscalYear.objects.all()
    serializer_class = FiscalYearSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['fiscal_year']
    ordering_fields = ['id']

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,FiscalYearPermission]    

class NoticeImagesViewSet(viewsets.ModelViewSet):
    queryset = NoticeImages.objects.all()
    serializer_class = NoticeImagesSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    authentication_classes = [JWTAuthentication]
    permission_classes = [NoticeImagesPermission] 


class ApprovedListViewSet(viewsets.ModelViewSet):
    queryset = ApprovedList.objects.all().order_by("-id")
    serializer_class = ApprovedListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    authentication_classes = [JWTAuthentication]
    permission_classes = [ApprovedListPermission] 

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ApprovedWriteSerializer
        return super().get_serializer_class()

class VerifiedListViewSet(viewsets.ModelViewSet):
    queryset = VerifiedList.objects.all().order_by("-id")
    serializer_class = VerifiedListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    authentication_classes = [JWTAuthentication]
    permission_classes = [VerifiedListPermission] 

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return VerifiedWriteSerializer
        return super().get_serializer_class()

