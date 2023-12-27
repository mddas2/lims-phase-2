from rest_framework import views
from management.models import SampleForm
from . final_serializer import CompletedSampleFormHasVerifierSerializer
from . analyst_final_report_serializer import CompletedSampleFormHasAnalystSerializer
from rest_framework.response import Response
from django.db.models import Q
from management import roles
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

cache_time = 300 # 300 is 5 minute

class FinalSampleFormHasVerifiedAPIView(generics.ListAPIView):
    # queryset = SampleForm.objects.all() 
    # serializer_class = CompletedSampleFormHasAnalystSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
  
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','name','owner_user','status','form_available','commodity__name','namuna_code','code']
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

    def get_queryset(self):
        user = self.request.user
  
        if user.role == roles.USER:
            query = SampleForm.objects.filter(owner_user=user.email).filter(Q(verifier__is_sent=True , verifier__is_verified=True , status="completed") | Q(status="rejected"))
        elif user.role == roles.SUPERVISOR:
            raise PermissionDenied("You do not have permission to access this resource.")
            query = SampleForm.objects.filter(Q(status="completed") | Q(status="not_verified")).filter(verifier__is_sent=True).filter(supervisor_sample_form__supervisor_user = user)

        elif user.role == roles.SMU:
            query = SampleForm.objects.filter(Q(verifier__is_sent=True, verifier__is_verified=True) | Q(status="rejected") | Q(status="recheck"))
        elif user.role == roles.SUPERADMIN:
            query = SampleForm.objects.filter(Q(verifier__is_sent=True, verifier__is_verified=True) | Q(status="rejected"))
        elif user.role == roles.ADMIN:
            query = SampleForm.objects.filter(Q(verifier__is_sent=True) & Q(verifier__is_verified=True) & Q(status="completed"))
        elif user.role == roles.ANALYST:
            # query = SampleForm.objects.filter(sample_has_parameter_analyst__analyst_user=user).filter(Q(sample_has_parameter_analyst__status='verified',sample_has_parameter_analyst__is_supervisor_sent=True) | Q(status="rejected"))
            query = SampleForm.objects.filter(sample_has_parameter_analyst__analyst_user=user).filter(Q(status = "completed") | Q(status="rejected"))

        elif user.role == roles.VERIFIER:
            query = SampleForm.objects.filter(verifier__is_sent=True)
            query = query.filter(Q(status="rejected") | Q(verifier__is_verified = True))
        else:
            raise PermissionDenied("You do not have permission to access this resource.")
        return query.order_by("-created_date")
    
    def get_serializer_class(self):
        if self.request.user.role == roles.ANALYST:
            serializer = CompletedSampleFormHasAnalystSerializer
        else:
            serializer = CompletedSampleFormHasVerifierSerializer
        return serializer
    
    @method_decorator(cache_page(150,key_prefix="SampleForm"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)