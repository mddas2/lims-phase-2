import os
from django.conf import settings
from django.http import HttpResponse
from rest_framework import views
try:
    import npttf2utf
except:
    pass
    #print("Please install npttf2utf")
    
from django.conf import settings

file_path = os.path.join(settings.STATIC_ROOT, "preeti_unicode_map/map.json")

class PreetiToUniCode(views.APIView):
    def get(self, request):        
        mapper = npttf2utf.FontMapper(file_path)
        unicode = mapper.map_to_unicode(';"gf}nf] sfkL pBf]u', from_font="Preeti", unescape_html_input=False, escape_html_output=False)
        # बकमानजवप            
        return HttpResponse(unicode)

class UnicodeToPreeti(views.APIView):
    def get(self,request):
        mapper = npttf2utf.FontMapper(file_path)
        preeti = mapper.map_to_preeti("सबिन आचार्य", from_font="unicode", unescape_html_input=False, escape_html_output=False)
        # ;lag cfrf/\o
        return HttpResponse(preeti)
        
        

