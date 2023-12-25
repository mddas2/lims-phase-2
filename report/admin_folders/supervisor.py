
from rest_framework import views,response
from management.models import SampleFormVerifier

class getStatusOfVerifierSampleForm(views.APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, sample_form_id, format=None):
        queryset = SampleFormVerifier.objects.filter(id=sample_form_id).first()
        if queryset.count()>0:
            return response({"found":True})
        else:
            return response({"found":True})