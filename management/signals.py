# signals.py

from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from management.models import RawDataSheet,SuperVisorSampleForm,SampleFormHasParameter,SampleForm,ClientCategory,SampleFormParameterFormulaCalculate,SampleFormVerifier
from websocket import frontend_setting
from account.models import CustomUser
from django.db import transaction
from django.db.models.signals import m2m_changed
# from datetime import datetime
from django.utils import timezone
from websocket.handle_notification import sampleFormNotificationHandler
from django.db.models import Q
from . import additional_data
from emailmanagement.sendmail_final_report import sendFinalreport

@receiver(post_save, sender=SampleFormParameterFormulaCalculate)
def SampleFormParameterFormulaCalculatePreSave(sender, instance,created, **kwargs):
    
    sample_form_obj = instance.sample_form    
    parameter_obj = instance.parameter

    sample_form_has_parameter = SampleFormHasParameter.objects.filter(sample_form_id = sample_form_obj.id,parameter = parameter_obj.id)   
    if sample_form_has_parameter.first().status == "pending":
        # sampleFormNotificationHandler(instance,"update","SampleFormHasParameter","Analyst started testing sample form "+instance.id ,"particular message ","SUPERVISOR","ANALYST from message")
        sample_form_has_parameter.update(status="processing")
        
    
@receiver(pre_save, sender=SampleForm)
def handle_sampleform_presave(sender, instance, **kwargs):
    original_sample_form_status = None
    if not instance.pk:
        client_category = instance.client_category_detail.client_category.id
        client_sub_caategory = instance.client_category_detail.client_sub_category

        if client_category == additional_data.dftqc_section:
            if client_sub_caategory in additional_data.client_sub_category_choices:
                count_data = SampleForm.objects.filter(client_category_detail__client_sub_category = client_sub_caategory).count()+1000
                encoded_data = additional_data.client_sub_category_dict[client_sub_caategory]
                full_encoded = encoded_data.upper() + "-" +str(count_data)
                instance.sample_symbol_number = full_encoded
                instance.new_name = instance.name
                instance.name = instance.name+f'({full_encoded})'
                # print(instance.name,instance.new_name)
    
    else:
        if instance.status == "completed":
            instance.completed_date = timezone.now()
            instance.approved_date = timezone.now()
        
    if instance.id:
        original_sample_form_status = SampleForm.objects.get(pk=instance.id).supervisor_user

    if instance.status != original_sample_form_status: # dynamic rawdata sheet status changing
        raw_data_obj = RawDataSheet.objects.filter(sample_form_id = instance.id).filter(~Q(status="recheck") or ~Q(status="re-assign"))
        raw_data_obj.update(status = instance.status)
            
@receiver(post_save, sender=SampleForm)
def handle_sampleform_presave(sender, instance ,created , **kwargs):
    if instance.status == "completed":
        sampleFormNotificationHandler(instance,"approved_sample_form")
        sendFinalreport(instance)
    if created:
        sampleFormNotificationHandler(instance,"new_sample_form")
        
        #send mail

@receiver(m2m_changed, sender=SampleFormHasParameter.parameter.through)
def sample_form_has_parameter_m2m_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    super_visor_sample_form_obj = instance.super_visor_sample_form 

    instance.is_supervisor_sent = False #blunder error fixed
    instance.status="processing"
    instance.save()

    status = "not_assigned"
    is_analyst_test = True
    
    parameters = super_visor_sample_form_obj.parameters.all()

    for param in parameters:    
        sample_form_has_parameter_object = SampleFormHasParameter.objects.filter(sample_form = instance.sample_form,parameter = param.id)
        
        if sample_form_has_parameter_object.exists():
            status = "processing"
            if sample_form_has_parameter_object.first().is_supervisor_sent == True:
                pass
            else:
                is_analyst_test = False
                
        else:
            status = "not_assigned"
            is_analyst_test = False
            break

    super_visor_sample_form_obj.status = status   
    super_visor_sample_form_obj.is_analyst_test = is_analyst_test
    super_visor_sample_form_obj.save()

@receiver(post_save, sender=SampleFormHasParameter)
def SampleFormHasParameterAfterSave(sender, instance ,created , **kwargs):
    if created:
        sampleFormNotificationHandler(instance,"assigned_analyst")
    if instance.is_supervisor_sent == True:
        super_visor_sample_form_obj = instance.super_visor_sample_form
        
        is_analyst_test_param = False
    
        sample_form_status = "processing"
        for parame in super_visor_sample_form_obj.parameters.all():
            sample_form_has_parame_obj =  SampleFormHasParameter.objects.filter(sample_form = instance.sample_form.id,parameter=parame)
            
            if sample_form_has_parame_obj.exists():
                if sample_form_has_parame_obj.first().is_supervisor_sent == True:
                    is_analyst_test_param = True
                    sample_form_status = "Test Completed"
                else:
                    is_analyst_test_param = False
                    sample_form_status = "processing"
                    break
            else:
                break
           
    
        # sample_form_status = "processing"
 
        if is_analyst_test_param == False:
            SuperVisorSampleForm.objects.filter(id=super_visor_sample_form_obj.id).update(is_analyst_test = is_analyst_test_param,status=sample_form_status,is_supervisor_sent = False)
        else:
            SuperVisorSampleForm.objects.filter(id=super_visor_sample_form_obj.id).update(is_analyst_test = is_analyst_test_param,status=sample_form_status)
        if is_analyst_test_param == True:
            supervisor_objs = SuperVisorSampleForm.objects.filter(sample_form = instance.sample_form.id)
            sup_is_analyst_test = False
            sup_status = "processing"
           
            for supervisor_obj in supervisor_objs: # if all supervisor analyst_test is True then update in sample form is_analyst_test = True
             
                if supervisor_obj.is_analyst_test == True:
                    sup_is_analyst_test = True
                    sup_status = "not_verified"
                else:
                    sup_is_analyst_test = False
                    sup_status = "processing"
                    break
            
            if sup_is_analyst_test:
                pass
                # from here sample form sent to verifier , is_analyst_test True, status = not_verified
                #SampleForm.objects.filter(id=instance.sample_form.id).update(is_analyst_test = sup_is_analyst_test,status=sup_status)
                    
        else:
            pass
            #print("all parameter has not assigned...")

    if instance.is_supervisor_sent == False:
        SampleForm.objects.filter(id=instance.sample_form.id).update(is_analyst_test = False,status="processing")
        
@receiver(m2m_changed, sender=SuperVisorSampleForm.parameters.through)
def supervisor_sample_form_has_parameter_m2m_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    
    instance.is_supervisor_sent = False #blunder error fixed
    instance.status="not_assigned"
    instance.is_analyst_test = False
    instance.save()

    status = "not_assigned"
 
    parameters = instance.parameters.all()

    for param in parameters:    
        sample_form_has_parameter_object = SuperVisorSampleForm.objects.filter(sample_form = instance.sample_form,parameters = param.id)
        
        if sample_form_has_parameter_object.exists():
            status = "processing"
                
        else:
            status = "not_assigned"
            sample_form_obj= instance.sample_form
            sample_form_obj.status = status
            sample_form_obj.is_analyst_test = False
            # sample_form_obj.form_available = 'smu'
            sample_form_obj.save()
            break

# @receiver(pre_save, sender=SuperVisorSampleForm)
# def SampleFormHasVerifierPostSave(sender, instance , **kwargs):
#     if instance.is_supervisor_sent == True:
#         instance.status = "not_verified"
#         print(instance.status)

@receiver(post_save, sender=SuperVisorSampleForm)
def SupervisorHaveParameterAfterSave(sender, instance , created , **kwargs):
    print(instance.status, " supervisor instance status")
    if created:
        sampleFormNotificationHandler(instance,"assigned_supervisor")

    if instance.is_supervisor_sent == True:      
     
        supervisor_objs = SuperVisorSampleForm.objects.filter(sample_form = instance.sample_form.id)
        sup_is_analyst_test = False
        sup_status = "processing"
        
        supervisor_param = 0
        for supervisor_obj in supervisor_objs: # if all supervisor analyst_test is True then update in sample form is_analyst_test = True
            param = supervisor_obj.parameters.all().count()
            supervisor_param = supervisor_param + param            
            check = supervisor_obj.is_supervisor_sent
            if check == True:
                sup_is_analyst_test = True
                sup_status = "not_verified"
            else:
                sup_is_analyst_test = False
                sup_status = "processing"
                break
        # print(sup_status, " verifier sup status \n")
        sample_obj_param = instance.sample_form.parameters.all().count()
       
        if sup_is_analyst_test == True and sample_obj_param == supervisor_param:
            data = {
                'is_verified':False,
                'is_sent':True,
            }
            verifier_obj,created = SampleFormVerifier.objects.update_or_create(sample_form_id = instance.sample_form_id,defaults=data)
            if created or verifier_obj != None:
                # print("reached to verifier")
                SampleForm.objects.filter(id=instance.sample_form.id).update(is_analyst_test = sup_is_analyst_test,status=sup_status)
                

        elif instance.is_supervisor_sent == False:
            if sample_obj_param == supervisor_param:
                status = "processing"
                form_available = "supervisor"
            else:
                status = "not_assigned"
                form_available = "smu"
            SampleForm.objects.filter(id=instance.sample_form.id).update(is_analyst_test = False,status=status,form_available = form_available)

@receiver(pre_save, sender=SampleFormHasParameter)
def SampleFormHasParameterAfterSave(sender, instance , **kwargs):
    if not instance.pk:
        instance.status = "pending"
    else:
        if instance.is_supervisor_sent == True:
            SampleFormParameterFormulaCalculate.objects.filter(sample_form_has_parameter_id = instance.pk,is_locked = False).update(is_locked = True)
        # sampleFormNotificationHandler(instance,"assigned_analyst")
        
@receiver(post_save, sender=SampleFormVerifier)
def SampleFormHasVerifierPostSave(sender, instance ,created , **kwargs):
    if created:
        sampleFormNotificationHandler(instance,"assigned_verifier")

@receiver(pre_save, sender=SampleFormVerifier)
def SampleFormHasVerifierPreSave(sender, instance, **kwargs):
    sample_form_obj = instance.sample_form
    if not instance.pk:  
        sample_form_obj.form_available = "verifier"
        sample_form_obj.status = "not_verified"
        sample_form_obj.save()
    else:        
        if instance.is_verified == True:
            sample_form_has_parameter_obj = sample_form_obj.sample_has_parameter_analyst
            sample_form_has_parameter_obj.update(status = "verified")
            
            supervisor_sample_form_obj = sample_form_obj.supervisor_sample_form
            supervisor_sample_form_obj.update(status = "verified")

            sample_form_obj.status = "not_approved"
            
            sample_form_obj.verified_date = timezone.now()

            sample_form_obj.remarks = instance.remarks
            sample_form_obj.save()

            sampleFormNotificationHandler(instance,"assigned_admin")

            


