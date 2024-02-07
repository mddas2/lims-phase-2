from django.http import HttpResponse
from django.template.loader import get_template


def FinalReport(request):
    return HttpResponse("final report")