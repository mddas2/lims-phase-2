from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group, Permission
from account.models import CustomUser
from rest_framework import viewsets
from .serializers import GroupNamesSerializer,PermissionGroupSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response

class PermissionHasGroupViewSet(viewsets.ViewSet):    
    serializer_class = GroupNamesSerializer
    def list(self, request):        
        permissions = Permission.objects.all().prefetch_related('group_set')
        permission_groups = []
        for permission in permissions:
            groups = permission.group_set.all()
            total_groups = Group.objects.all()
            group_dict = {}
                    
            for tot_groups in total_groups:           
                if tot_groups in groups:
                    group_dict[tot_groups.name] = tot_groups.permissions.filter(id=permission.id).exists()
                else:
                    group_dict[tot_groups.name] = False
 
            permission_groups.append({'permission_id': permission.id,'name':permission.name,'codename':permission.codename, 'groups': group_dict})
        return Response(permission_groups)
    
    def retrieve(self,request,pk=None):
        try:
            permission = Permission.objects.get(pk=pk)
        except Permission.DoesNotExist:
            return Response({"error": "Permission not found."}, status=404)

        groups = permission.group_set.all()

        group_dict = {}
        for group in groups:
            group_dict[group.name] = group.permissions.filter(id=permission.id).exists()
       
        serializer = GroupNamesSerializer(data={'group_names': list(group_dict.keys())})
       
        if serializer.is_valid():
            return Response({'permission_id': permission.id, 'name':permission.name,'codename':permission.codename, 'groups': group_dict}, status=200)
        else:
            return Response(serializer.errors, status=400)

    def create(self,request):
        serializer = PermissionGroupSerializer(data=request.data)

        if serializer.is_valid():
            permission_id = serializer.validated_data['permission_id']
            group_data = serializer.validated_data['groups']
            try:
                permission = Permission.objects.get(id=permission_id)
            except Permission.DoesNotExist:
                return Response({"error": "Permission not found."}, status=404)

            groups = Group.objects.filter(name__in=group_data.keys())
            for group in groups:
                if group_data[group.name]:
                    group.permissions.add(permission)
                else:
                    group.permissions.remove(permission)

            return Response({'message': True}, status=201)
        else:
            return Response(serializer.errors, status=400)
        
def CustomPermissionInsert(request):
    
    from django.contrib.auth.models import Permission, ContentType
    from account.models import CustomUser
    from management.models import Commodity, SampleForm, ClientCategory
    Permission.objects.all().delete()
    sample_form_content_type = ContentType.objects.get_for_model(SampleForm)
    user_content_type = ContentType.objects.get_for_model(CustomUser)
    commodity_content_type = ContentType.objects.get_for_model(Commodity)
    client_category_content_type = ContentType.objects.get_for_model(ClientCategory)

    permissions = [
        (1, 'can update sample form', 'can_update_sample_form', sample_form_content_type),
        (2, 'can delete sample form', 'can_delete_sample_form', sample_form_content_type),
        (3, 'can create sample form', 'can_create_sample_form', sample_form_content_type),
        (4, 'can half view sample form', 'can_half_view_sample_form', sample_form_content_type),
        (5, 'can full view sample form', 'can_full_view_sample_form', sample_form_content_type),

        (6, 'can modify commodity', 'can_modify_commodity', commodity_content_type),
        (7, 'can modify client category', 'can_modify_client_category', client_category_content_type),

        (8, 'can access user', 'can_access_users', user_content_type),
        (9, 'can modify user', 'can_modify_users', user_content_type),
        (10, 'can modify user role permission', 'can_modify_user_role_permission', user_content_type),

        (11, 'can assign supervisor', 'can_assign_supervisor', user_content_type),
        (12, 'can assign analyst', 'can_assign_analyst', user_content_type),
    ]

    for id, name, codename, content_type_id in permissions:
        data = {
            'name': name,
            'codename': codename,
            'content_type_id': content_type_id.id,
        }

        obj, created = Permission.objects.update_or_create(id=id, defaults=data)
        if created:
            pass
            # print(obj)


    from django.http import HttpResponse
    # http://127.0.0.1:8000/api/account/add-customized-permission/
    return HttpResponse("all permission deleted and add customized permission 123...")
        



    
  
