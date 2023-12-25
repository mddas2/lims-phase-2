import json
from account.models import CustomUser
from management.models import SampleForm,Commodity,SampleFormHasParameter,CommodityCategory
# from . serializers import CustomUserSerializer,CommodityCategorySerializer,SampleFormOnlySerializer,CommodityOnlySerializer,ClientCategorySerializer
from django.http import HttpResponse
import pandas as pd
from management import roles
from datetime import date
from django.template.loader import get_template
from xhtml2pdf import pisa
from management.models import SampleFormParameterFormulaCalculate
from management.encode_decode import generateDecodeIdforSampleForm,generateAutoEncodeIdforSampleForm,generateDecodeIdByRoleforSampleForm
from management.raw_data_serializer import rawDataTestTypeGlobalSerializer

from account.department_type import department_code
from rest_framework.response import Response
from management.models import RawDataSheet

import qrcode
import os
from django.shortcuts import render
from django.conf import settings
from django.templatetags.static import static
# https://limsserver.kantipurinfotech.com.np/api/report/get-report/report_name/report_type/report_lang/
def ReportAdminList(report_type,report_lang,id=None):
    query = CustomUser.objects.all()
    serializer_data = CustomUserSerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    if report_type == "excel":
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    
    elif report_type == "pdf":
        # #print("pdf")
        return HttpResponse("<html><body> this is report admin list pdf download </body></html>")


def ReportUserList(report_type,report_lang,id=None):
    query = CustomUser.objects.all()
    serializer_data = CustomUserSerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    if report_type == "excel":
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    
    elif report_type == "pdf":
        # #print("pdf")
        return HttpResponse("<html><body> this is report user  list pdf download </body></html>")

def ReportUserRequest(report_type,report_lang,id=None):
    query = CustomUser.objects.filter(is_verified = False)
    serializer_data = CustomUserSerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    if report_type == "excel":
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    
    elif report_type == "pdf":
        # #print("pdf")
        return HttpResponse("<html><body> this is report user  request pdf download </body></html>")
    


def ReportUserSampleForm(report_type,report_lang,id=None):
    query = SampleForm.objects.all()
    serializer_data = SampleFormOnlySerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    if report_type == "excel":
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    
    elif report_type == "pdf":
        # #print("pdf")
        return HttpResponse("<html><body> this is report user has sample form pdf download </body></html>")

def ClientCategory(report_type,report_lang,id=None):
    from management.models import ClientCategory
    query = ClientCategory.objects.all()
    serializer_data = ClientCategorySerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    if report_type == "excel":
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    
    elif report_type == "pdf":
        # #print("pdf")
        return HttpResponse("<html><body> this is report client category form pdf download </body></html>")


def ReportSampleForm(report_type,report_lang,id=None):
    query = SampleForm.objects.all()
    serializer_data = SampleFormOnlySerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    # Create a response object with the appropriate content type
    if report_type == "excel":
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    
    elif report_type == "pdf":
        # #print("pdf")
        return HttpResponse("<html><body> this is report sample form pdf download </body></html>")

def ReportCommodity(report_type,report_lang,id=None):
    query = Commodity.objects.all()
    serializer_data = CommodityOnlySerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    # Create a response object with the appropriate content type
    if report_type == "excel":
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    
    elif report_type == "pdf":
        # #print("pdf")
        return HttpResponse("<html><body> this is report commodity pdf download </body></html>")

def ReportComodityCategory(report_type,report_lang,id=None):
    query = CommodityCategory.objects.all()
    serializer_data = CommodityCategorySerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    # Create a response object with the appropriate content type
    if report_type == "excel":
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    
    elif report_type == "pdf":
        # #print("pdf")
        return HttpResponse("<html><body> this is report commodity category pdf download </body></html>")


def ReportParameter(report_type,report_lang,id=None):
    query = Commodity.objects.all()
    serializer_data = CommodityOnlySerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    if report_type == "excel":
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    
    elif report_type == "pdf":
        # #print("pdf")
        return HttpResponse("<html><body> this is report admin list pdf download </body></html>")


def FinalReport(request,report_type,report_lang,id=None,role=None):
    from rest_framework.response import Response

    encoded_id = id
    id = generateDecodeIdByRoleforSampleForm(id,role)

    if id == None:
        return Response({'error':"please provide http://127.0.0.1:8000/api/report/get-report/final-report/pdf/eng/id/ or unvalid id","statu":400})
    try:
        query = SampleForm.objects.get(id = id)
    except:
        return HttpResponse("You are trying to access with sample form with other id")

    try:
        if query.verifier.is_verified == False:
            return Response({'error':"Sample Form have not verified","statu":400})
    except:
        return Response({'error':"Sample Form have not verified","statu":400})



    # Create a response object with the appropriate content type
    if report_type == "excel":
        serializer_data = SampleFormOnlySerializer(query, many=True)
        serialized_data = serializer_data.data
        df = pd.DataFrame.from_records(serialized_data)
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response

    elif report_type == "pdf":
        # Load the HTML template
        # if role ==  roles.USER:
        #     template = get_template('final_user_report.html')
        # else:
        #     template = get_template('final_report.html')
        template = get_template('final_report.html')

        # Define the context data
        sample_form_name = query.name
        symbol_number = ''
        mfd = query.mfd
        batch = query.batch
        remarks = query.remarks
        brand = query.brand
        condition = query.condition
        department_address = ''
        try:
            user_obj = CustomUser.objects.get(email = query.owner_user)
            owner_name = user_obj.first_name
            department_address = user_obj.department_address
            department_address = getDepartmentValue(department_address) 
            owner_name = user_obj.department_name #
        except:
            owner_name = query.owner_user

        client_categoty = query.client_category_detail.client_category
        if str(client_categoty.id) == "11":
            owner_name = "Liscensing and Inspection section  </br> Food and Feet Sanitation and Quality Control Division </br> Food Technology and Quality Control Department </br> Babarmahal,Kathmandu"
            department_address = ""
            symbol_number = "</br>"+sample_form_name
            sample_form_name = query.commodity.name
        
                       


        sample_registration_date = query.created_date.date()
        sample_code = query.refrence_number
        analysis_starting_date = query.created_date.date()
        analysis_completion_date = query.created_date.date()

        parameters = query.result.all()

        qr_code_image_url = generateQrcode(query.id,request)
        context = {
           'qr_code_image_url':qr_code_image_url,
           'symbol_number':symbol_number,
           'sample_form_name' : sample_form_name,
           'remarks':remarks,
           'department_address' : department_address,
           'condition':condition,
           'owner_name' : owner_name,
           'sample_registration_date':sample_registration_date,
           'sample_code':sample_code,
           "analysis_starting_date":analysis_starting_date,
           "analysis_completion_date":analysis_completion_date,
           'parameters':parameters,
           'mfd':mfd,
           'brand':brand,
           'batch':batch
        }

        # Render the template with the context
        html = template.render(context)

        # Create a PDF object
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="output.pdf"'

        # Generate the PDF from the HTML contents
        pisa.CreatePDF(html, dest=response)
        return response


def getDepartmentValue(key):
    for code, k_value in department_code:
        if code == key:
            return k_value
    return key

def rawDataSheetAnalystReport(request,download_print,sample_form_has_param):
    
    try:
        raw_data = RawDataSheet.objects.filter(id = sample_form_has_param)
        test_type = raw_data.first().test_type
    except:
        raw_data = RawDataSheet.objects.filter(sample_form_has_parameter_id = sample_form_has_param)
        test_type = raw_data.first().test_type

    if test_type == "Microbiological":
        template = get_template('raw_data_micro.html')
        context = {
            'raw_data':raw_data.first(),
            'sample_form':raw_data.first().sample_form,
        }
    else:
        serializer_data = rawDataTestTypeGlobalSerializer(raw_data,many=True)
        return Response(serializer_data.data)
        template = get_template('raw_data.html')
        context = {
            'raw_data':raw_data,
            'sample_form':raw_data.first().sample_form
        }

    # Render the template with the context
    html = template.render(context)

    # Create a PDF object
    response = HttpResponse(content_type='application/pdf')

    if download_print == "print":
        response['Content-Disposition'] = 'inline; filename="output.pdf"'
    elif download_print == "download":
        response['Content-Disposition'] = 'attachment; filename="output.pdf"'
    else:
        response['Content-Disposition'] = 'inline; filename="output.pdf"'

    # Generate the PDF from the HTML content
    pisa.CreatePDF(html, dest=response)

    return response

def TestReport(request,report_type,report_lang,sample_form_has_param,role):
    from rest_framework.response import Response
    
    
    # id = generateDecodeIdByRoleforSampleForm(sample_form_id,role)
    id =  sample_form_has_param

    if id == None:
        return Response({'error':"please provide http://127.0.0.1:8000/api/report/get-report/final-report/pdf/eng/id/ or unvalid id","statu":400})
    try:
        query = SampleFormHasParameter.objects.get(id = id)
    except:
        return HttpResponse("You are trying to access with sample form with other id")

    sample_form = query.sample_form
  
    parameters = SampleFormParameterFormulaCalculate.objects.filter(sample_form_has_parameter = query.id)
        
    template = get_template('testreportsheet.html')
    context = {
            'sample_form':sample_form,
            'parameters':parameters,
            'sample_form_has_parameter':query
        }

    
    html = template.render(context)

    # Create a PDF object
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'inline; filename="output.pdf"'
  

    # Generate the PDF from the HTML content
    pisa.CreatePDF(html, dest=response)

    return response

def generateQrcode(id,request):
    data = request.build_absolute_uri() 
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to the media directory with dynamic name
    image_name = f"{id}.png"
    image_path = os.path.join(settings.MEDIA_ROOT, "qr_codes", image_name)

    if not os.path.exists(os.path.dirname(image_path)):
        os.makedirs(os.path.dirname(image_path))
    try:
        img.save(image_path)
    except Exception as e:
        pass
        #print("Error saving image:", e)

    image_url = f"media/qr_codes/{image_name}"

    return image_url
