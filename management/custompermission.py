from rest_framework.permissions import BasePermission
from . import roles

def IsAuthenticated(request):
    return bool(request.user and request.user.is_authenticated)

def SMU_USER_Permission(request):
    return IsAuthenticated(request) and request.user.role in [roles.SMU ,roles.USER]

def SmuSuperAdmin(request):
    return IsAuthenticated(request) and request.user.role in [roles.SMU ,roles.SUPERADMIN]

def fullAdminPermission(request):
    return IsAuthenticated(request) and request.user.role in [roles.ADMIN, roles.SMU , roles.SUPERADMIN, roles.VERIFIER,roles.SUPERVISOR,roles.ANALYST]

def allAdminPermission(request):
    return IsAuthenticated(request) and request.user.role in [roles.ADMIN, roles.SMU , roles.SUPERADMIN, roles.VERIFIER]

def AdminLevelPermission(request):
    return IsAuthenticated(request) and request.user.role in [roles.ADMIN, roles.SMU , roles.SUPERADMIN]

def AnalystPermission(request):
    return IsAuthenticated(request) and request.user.role in [roles.ANALYST]

def VerifierLevelPermission(request):
    return IsAuthenticated(request) and request.user.role in [roles.VERIFIER]

def SuperVisorLevelPermission(request):
    return IsAuthenticated(request) and request.user.role in [roles.SUPERVISOR]

def SmuSuperVisorLevelPermission(request):
    return IsAuthenticated(request) and request.user.role in [roles.SUPERVISOR,roles.SMU]

def SuperVisorAnalystLevelPermission(request):
    return IsAuthenticated(request) and request.user.role in [roles.SUPERVISOR,roles.ANALYST]

def SuperAdminLevelPermission(request):
    return IsAuthenticated(request) and request.user.role in [roles.SUPERADMIN]

def AdminLevelPermission(request):
    return IsAuthenticated(request) and request.user.role in [roles.ADMIN]


def AdminSuperAdminLevelPermission(request):
    return IsAuthenticated(request) and request.user.role in [roles.ADMIN,roles.SUPERADMIN]

def VerifierSuperAdminLevelPermission(request):
    return IsAuthenticated(request) and request.user.role in [roles.VERIFIER,roles.SUPERADMIN]

class SampleFormViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return True
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return SMU_USER_Permission(request)
        elif method_name == 'partial_update':
            #print("SDasd asd")
            return allAdminPermission(request)
        elif method_name == 'destroy':
            return False
        else:
            return False
        
class SuperVisorSampleFormViewsetPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return SmuSuperVisorLevelPermission(request)
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return SmuSuperVisorLevelPermission(request)
        elif method_name == 'partial_update':
            return SmuSuperVisorLevelPermission(request)
        elif method_name == 'destroy':
            return False
        else:
            return False

class CommodityViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return AdminSuperAdminLevelPermission(request)
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return AdminSuperAdminLevelPermission(request)
        elif method_name == 'partial_update':
            return AdminSuperAdminLevelPermission(request)
        elif method_name == 'destroy':
            return False
        else:
            return False
        
class MicroparameterViewsetPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return AnalystPermission(request)
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return AnalystPermission(request)
        elif method_name == 'partial_update':
            return AnalystPermission(request)
        elif method_name == 'destroy':
            return False
        else:
            return False
        
class FiscalYearPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if request.user.role != roles.SUPERADMIN:
            return False

        if method_name == 'list':
            return True
        elif method_name == 'create':
            return True
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return True
        elif method_name == 'partial_update':
            return False
        elif method_name == 'destroy':
            return False
        else:
            return False
        
class RejectSampleFormViewSetPermission(BasePermission):
    def has_permission(self, request, view):
    
        print(" checked permission for Reject")
        return allAdminPermission(request)
    
        
class ParameterHasResultRecheckPermission(BasePermission):
    def has_permission(self, request, view):

        print(" checked permission for parameter recheck")
        return SuperVisorLevelPermission(request)
    

class SampleFormRecheckPermission(BasePermission):
    def has_permission(self, request, view):
       
        print(" checked permission for recheck")
        return SmuSuperAdmin(request)
        
        
class CommodityCategoryViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return AdminSuperAdminLevelPermission(request)
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return AdminSuperAdminLevelPermission(request)
        elif method_name == 'partial_update':
            return AdminSuperAdminLevelPermission(request)
        elif method_name == 'destroy':
            return False
        else:
            return False
        
class TestResultViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return AdminSuperAdminLevelPermission(request)
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return AdminSuperAdminLevelPermission(request)
        elif method_name == 'partial_update':
            return AdminSuperAdminLevelPermission(request)
        elif method_name == 'destroy':
            return False
        else:
            return False
        
class PaymentViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return SmuSuperAdmin(request)
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return SmuSuperAdmin(request)
        elif method_name == 'partial_update':
            return SmuSuperAdmin(request)
        elif method_name == 'destroy':
            return False
        else:
            return False
        
class SampleFormHasVerifierViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return VerifierLevelPermission(request)
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return VerifierLevelPermission(request)
        elif method_name == 'partial_update':
            return VerifierLevelPermission(request)
        elif method_name == 'destroy':
            return False
        else:
            return False

class ClientCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return False
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return False
        elif method_name == 'partial_update':
            return False
        elif method_name == 'destroy':
            return False
        else:
            return False
        
class SampleFormHasParameterPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return SuperVisorAnalystLevelPermission(request)
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return SuperVisorAnalystLevelPermission(request)
        elif method_name == 'partial_update':
            return SuperVisorAnalystLevelPermission(request)
        elif method_name == 'destroy':
            return False
        else:
            return False

class NoticeImagesPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return fullAdminPermission(request)
        elif method_name == 'create':
            return SuperVisorLevelPermission(request)
        elif method_name == 'retrieve':
            return fullAdminPermission(request)
        elif method_name == 'update':
            return SuperVisorLevelPermission(request)
        elif method_name == 'partial_update':
            return SuperVisorLevelPermission(request)
        elif method_name == 'destroy':
            return SuperVisorLevelPermission(request)
        else:
            return False
        
class ApprovedListPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return AdminSuperAdminLevelPermission(request)
        elif method_name == 'create':
            return SuperAdminLevelPermission(request)
        elif method_name == 'retrieve':
            return AdminSuperAdminLevelPermission(request)
        elif method_name == 'update':
            return SuperAdminLevelPermission(request)
        elif method_name == 'partial_update':
            return SuperAdminLevelPermission(request)
        elif method_name == 'destroy':
            return SuperAdminLevelPermission(request)
        else:
            return False
        
class VerifiedListPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return VerifierSuperAdminLevelPermission(request)
        elif method_name == 'create':
            return SuperAdminLevelPermission(request)
        elif method_name == 'retrieve':
            return VerifierSuperAdminLevelPermission(request)
        elif method_name == 'update':
            return SuperAdminLevelPermission(request)
        elif method_name == 'partial_update':
            return SuperAdminLevelPermission(request)
        elif method_name == 'destroy':
            return SuperAdminLevelPermission(request)
        else:
            return False
        


    

