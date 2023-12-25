import json
from account.models import CustomUser
from management.models import SampleForm,Commodity,SampleFormHasParameter,CommodityCategory
from . serializers import CustomUserSerializer,CommodityCategorySerializer,SampleFormOnlySerializer,CommodityOnlySerializer,ClientCategorySerializer
from django.http import HttpResponse
import pandas as pd
from management import roles
from datetime import date
from django.template.loader import get_template
from xhtml2pdf import pisa
from management.encode_decode import generateDecodeIdforSampleForm,generateAutoEncodeIdforSampleForm,generateDecodeIdByRoleforSampleForm
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
            
        sample_registration_date = query.created_date.date()
        sample_code = query.refrence_number
        analysis_starting_date = query.created_date.date()
        analysis_completion_date = query.created_date.date()

        parameters = query.result.all()

        # print(parameters)
        qr_code_image = generateQrcode(1)
        # return HttpResponse(image)
        context = {
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
           'batch':batch,
           'qr_code_image':qr_code_image
        }

        
        # Render the template with the context
        html = template.render(context)

        # Create a PDF object
        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="output.pdf"'

        # Generate the PDF from the HTML content
        pisa.CreatePDF(html, dest=response)

        return response
    
from account.department_type import department_code

def getDepartmentValue(key):
    for code, k_value in department_code:
        if code == key:
            return k_value
    return key

def rawDataSheetAnalystReport(request,download_print,sample_form_has_param):
    from rest_framework.response import Response
    from management.models import RawDataSheet

    # raw_data =     
    template = get_template('raw_data.html')

    raw_data = RawDataSheet.objects.filter(id = sample_form_has_param)

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

def generateQrcode(sample_form_id):
    import qrcode
    import base64
    from io import BytesIO
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data("https://example.com")  # Set the data for the QR code
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Convert the QR code image to a Base64 string
    buffer = BytesIO()
    qr_image.save(buffer, format='PNG')
    qr_code_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return qr_code_image_base64