from django.shortcuts import render
from rest_framework import viewsets
from . models import Notification
from rest_framework import status
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .pagination import MyLimitOffsetPagination
from rest_framework.response import Response
from . serializer import NotificationWriteSerializer,NotificationReadSerializer
from django_filters.rest_framework import DjangoFilterBackend
from management import roles
from django.db.models import Q

# Create your views here.
class NotificationViewSet(viewsets.ModelViewSet):

    queryset = Notification.objects.all().order_by("-created_date")
    serializer_class = NotificationReadSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    filterset_fields = ['id']
    search_fields = ['id']

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    pagination_class = MyLimitOffsetPagination

    
    def get_queryset(self):
        user = self.request.user
        query = Notification.objects.filter(to_notification = user)      
        return query.order_by("-created_date")
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return NotificationWriteSerializer
        return super().get_serializer_class()
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "Notification created successfully",
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
            "message": "Notification updated successfully",
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
            "message": "Notification category deleted successfully"
        }

        # Return the custom response
        return Response(response_data)
