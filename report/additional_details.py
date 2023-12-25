from management.models import SampleForm
from rest_framework.response import Response
from django.db.models import Q
from management import roles
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .serializers.additional_serializers import SampleFormSerializer

class AdditionalDetailSampleForm(generics.ListAPIView): #by sagar

    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['name','owner_user','status','form_available','commodity__name']
    ordering_fields = ['name','id']
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'owner_user': ['exact'],
        'status': ['exact'],
        'form_available': ['exact'],
        'commodity_id': ['exact'],
        'supervisor_user': ['exact'],
        'created_date': ['date__gte', 'date__lte']  # Date filtering
    }

    def get_queryset(self):
        query = SampleForm.objects.filter(client_category_detail__client_category_id = 1)   
        return query.order_by("-created_date")
    
    def get_serializer_class(self):
        return SampleFormSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)