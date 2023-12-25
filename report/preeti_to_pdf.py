from django.http import HttpResponse
import io
from reportlab.pdfgen import canvas
from io import BytesIO, StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.templatetags.static import static
from django.conf import settings

def PreetiToPdf(request):
    response = HttpResponse(content_type="application/pdf")
    d = datetime.today().strftime('%Y-%m-%d')
    response['Content Disposition'] = f'inline; filenane="{d}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas (buffer, pagesize=A4)

    #Data to print  
    # data = {
    # "Posts": [{"title":"Bython","Views" :500}, {"title": "JavaScript", "views":500}],
    # "Videos" :[{"title": "Python Prooramming", "Likes":500}],
    # "Blogs": [{"nane":"Report Lab","Likes":500, "claps":500}],
    # }

    # path = str(settings.BASE_DIR)+static("/preeti_unicode_map/Preeti-Font.ttf")
    # return HttpResponse(path)
    pdfmetrics.registerFont(TTFont("Preeti", str(settings.BASE_DIR)+static("/preeti_unicode_map/Preeti-Font.ttf")))

    # pdfmetrics.registerFont(TTFont("Preeti-Bold", settings.BASE_URL+static("/assets/fonts/Preeti-Bold.ttf")))
    # pdfmetrics.registerFont(TTFont("Times", settings.BASE_URL+static("/assets/fonts/Times.ttf")))
    
    # Start writing the POF here
    # p.setFillColorRGB(0, 0,0)
    # p.drawImage(settings.BASE_URL+static("/assets/images/logo-2.png"),30,740,550,75,mask='auto')
    # p.line(25, 730,575, 730)

    p.setFont("Preeti", 22, leading=None)
    p.drawString(450,690,"ldlt M") #miti

    # p.setFont("Times", 15, leading=None)
    # p.drawString(493,690,d) #date

    p.setFont("Preeti", 22, leading=None)
    p.drawString(25,650,">Ldfg cWoIfHo',") #xirman
    p.drawString(25,625,"g]kfn jg k}bfjf/ pBf]u Joj;foL ;+3")

    # p.setFont("Preeti-Bold", 22, leading=None)
    # p.drawString(200,550,"laifo M ;b:otf ;DaGwdf . ")#bisaya 550

    p.setFont("Preeti", 22, leading=None)
    p.drawString(100,505,"""jg k}bfjf/df cfwfl/t ;Dk'0f{ pBf]u Joj;foLx?sf] xslxt ;+/If0f / """) 
    p.drawString(25,480,"""k}/jL ug]{ o; lhNnf ;+3sf] ljwfgsf] clwgdf /lx gLlt, sfo{s|d tyf lg0f{ox?""") 
    p.drawString(25,455,"""k"0f{?kdf kfngf ug]{' kg]{ 5 . """) 

    # p.drawString(350,410,"""cWoIf M """) 
    # p.drawString(350,380,"""b:tvt M""") 
    # p.drawImage(settings.BASE_URL+static("/assets/images/signature.jpeg"),410,350,80,60,mask='auto') 



    #Render data
   

    p.setTitle(f'Report on {d}')
    p.showPage()
    # return HttpResponse("hello")
    p.save()
    pdf = buffer.getvalue()
    buffer. close()
    response.write(pdf) #hide if you return bytes
    return response
    # return pdf #if you return byte

# https://github.com/mddas2/Forest_Based_Industry_FENFIT_management_system/blob/0a4de045cdbd481fbf09e9a45f8ebd138d7f9bba/Admin/html_to_pdf.py