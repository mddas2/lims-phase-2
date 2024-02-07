from rest_framework.permissions import BasePermission

class AccountPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        # print(method_name)
        if method_name == 'list':
            return True
        elif method_name == 'create':
            #check 
            return True
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            #check update role , if  role is user then only can updte there own account. for update all role must be ADMIN
            return True
        elif method_name == 'partial_update':
            return True
        elif method_name == 'destroy':
            return False
        else:
            return False