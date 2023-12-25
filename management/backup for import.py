from django.http import FileResponse
from django.conf import settings
from django.http import HttpResponse
import os
from rest_framework.response import Response
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render,redirect
from .serializers import TestResultWriteSerializer
from .models import Commodity,CommodityCategory,TestResult,SampleForm,Units,MandatoryStandard,TestMethod
from django.contrib import messages

def ImportExcel(request):
    # CommodityCategory.objects.all().delete()
    # SampleForm.objects.all().delete()
    # return HttpResponse("deleted successfully!!!....")
    
    if request.POST:
        file = request.FILES.get('file')
    else:
        return render(request, 'excel_import.html')

    file_path = file
 
    df = pd.read_excel(file_path)
    total_rows = df.shape[0]
    already_exists_parameters = 0
    for index, row in df.iterrows():
        # print(index)
        commodity_category = row['commodity_category']
        commodity_category_nepali = row['commodity_cat_nepali']

        commodity_name = row['commodity_name']
        commodity_name_nepali = row['commodity_name_nepali']

        test_type = row['test_type']
        test_type = test_type.replace(" ", "")
        test_type_nepali = row['test_type_nepali']

        parameters_name = row['parameters']
      
        try:
            parameters_nepali = row['parameter_nepali']
        except:
            parameters_nepali = parameters_name

        ref_test_method = row['ref._test_methods']

        commodity_test_duration = row['commodity_test_duration']

        unit = row['units']
        unit_nepali = row['units_nepali']

        mandatory_standard = row['mandatory_standard']
    
        mandatory_standard_nepali = row['mandatory_standard_nepali']

        formula = row['formula']

        try:
            notation = row['abbreviation']
        except:
            notation = ""

        remarks = row['remarks']

        commodity_price = row['commodity_price']
        try:
            commodity_price = int(commodity_price)
        except:
            commodity_price = 0
        
        parameter_price = row['parameter_price']
        try:
            parameter_price = int(parameter_price)
        except:
            parameter_price = 0
    
        # return HttpResponse(parameter_price)

        commodity_category_data = {
            'name' : commodity_category,
            'name_nepali' : commodity_category_nepali,
        }


        try:
            commodity_category_obj = CommodityCategory.objects.create(**commodity_category_data)
        except:
            #print("can not create")
        commodity_category_id = CommodityCategory.objects.get(name=commodity_category).id
        commodity_data = {
            'category_id' : commodity_category_id,
            'name' : commodity_name,
            'name_nepali':commodity_name_nepali,
            'units' : unit,
            'price' : commodity_price,
            'test_duration' : commodity_test_duration,
        }
        commodity_obj,create = Commodity.objects.update_or_create(name = commodity_name, defaults= commodity_data)
        if create:
            #print("commodity created")

        multiple_units,multiple_mandatory_standard,multiple_ref_test_method = multipleUnitsMandatoryRefTestMethod(unit,unit_nepali,ref_test_method,mandatory_standard,mandatory_standard_nepali)

        commodity_id = Commodity.objects.get(name=commodity_name).id
        print(commodity_id," commodity obj")
        test_result = { #parameter
            'commodity' : commodity_id,
            'name' : parameters_name,
            'name_nepali' : parameters_nepali,
            'test_method' : multiple_ref_test_method,
            'units' : multiple_units,
            'price' : parameter_price,
            'mandatory_standard' : multiple_mandatory_standard,
            'remarks' : remarks,
            'test_type' : test_type,
            'test_type_nepali' : test_type_nepali,
            'formula_notation' : notation,
            'formula' : formula,
        }
        # print(test_result)

        param_update_or_create = TestResult.objects.filter(commodity_id = commodity_id ,name = parameters_name)
        print(multiple_ref_test_method," multiple_ref_test_method update or create. ")
        if param_update_or_create.exists():
            #print("already exists..")
            already_exists_parameters = already_exists_parameters + 1
            pass
        else:
            serializer = TestResultWriteSerializer(data=test_result)
            serializer.is_valid(raise_exception=True)
            serializer.save()

    messages.success(request, 'Data imported successfully.')
    total_create = total_rows-already_exists_parameters
    # return render(request, 'excel_import.html',data)
    return redirect('ResubmissionPrevent',total_rows,already_exists_parameters,total_create)

def multipleUnitsMandatoryRefTestMethod(unit,unit_nepali,ref_test_method,mandatory_standard,mandatory_standard_nepali):
    unit_data = {
        'units_nepali':unit_nepali,
    }
    unit_create_obj,unit_create = Units.objects.update_or_create(units = unit, defaults = unit_data)

    test_method_data = {
        'ref_test_method':ref_test_method
    }
    test_method_data_obj,test_method_create = TestMethod.objects.update_or_create(ref_test_method = ref_test_method, defaults = test_method_data)
    print(test_method_data_obj," crete orobject test method obj..")

    mandatory_standard_data = {
            'mandatory_standard_nepali':mandatory_standard_nepali
        }
    mandatory_standards_obj,mandatory_standard_data_create = MandatoryStandard.objects.update_or_create(mandatory_standard = mandatory_standard,defaults=mandatory_standard_data)


    if unit_create:
        unit_create_ids =  [unit_create_obj.id]
    else:
        unit_create_ids = [unit_create_obj.id]

    if test_method_create:
        test_method_create_ids =  [test_method_data_obj.id]
    else:
        test_method_create_ids = [test_method_data_obj.id]

    if mandatory_standard_data_create:
        mandatory_standard_data_create_ids =  [mandatory_standards_obj.id]
    else:
        mandatory_standard_data_create_ids = [mandatory_standards_obj.id]
    
    return unit_create_ids,mandatory_standard_data_create_ids,test_method_create_ids

def ResubmissionPrevent(request,total_rows,already_exists_parameters,total_create):
    data = {
        'total_rows':total_rows,
        'already_exists_parameters':already_exists_parameters,
        'total_create':total_create
    }
    return render(request, 'excel_import.html',data)
  