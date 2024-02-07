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


class GetStatus(views.APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
        
    def get(self, request, format=None,url=None):
        import json
        status = [
            {
                'name': 'Pending',
                'value': 'pending', 
            },
            {
                'name': 'Processing',
                'value': 'processing', 
            },
            {
                'name': 'Not Assigned',
                'value': 'not_assigned',
            },
            {
                'name': 'Not Verified',
                'value': 'not_verified',
            },
            {
                'name': 'Completed',
                'value': 'completed',
            },
            {
                'name': 'Recheck',
                'value': 'recheck',
            },
            {
                'name': 'Rejected',
                'value': 'rejected',
            }
        ]

        return Response(status)