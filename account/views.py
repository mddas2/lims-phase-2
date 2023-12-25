
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .serializers import LoginSerializer
from django.contrib.auth.models import Group, Permission
from account.models import CustomUser,CustomUserImages
from rest_framework import viewsets
from .serializers import CustomUserReadSerializer,CustomUserSerializer, GroupSerializer, PermissionSerializer,RoleSerializer,departmentTypeSerializer,CustomUserReadLimitedSerializer,userAdminLevelDataSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from management import roles
from rest_framework.exceptions import PermissionDenied
from . import department_type
from websocket.handle_notification import NotificationHandler
from django.http import HttpResponse
from django.db.models import Q
from rest_framework import generics
from .custompermission import AccountPermission
from . serializers import CustomUserImageSerializer

from django.core.cache import cache
cache_time = 300 # 300 is 5 minute

class CustomUserSerializerViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    # permission_classes = [Account]
    serializer_class = CustomUserReadSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','email','username','first_name','last_name','is_verified','phone','department_name']
    ordering_fields = ['username','id']
    filterset_fields = {
        'email': ['exact', 'icontains'],
        'username': ['exact'],
        'is_verified': ['exact'],
        'is_reject': ['exact'],
        'role': ['exact'],
        'client_category_id': ['exact'],
        'created_date': ['date__gte', 'date__lte'],  # Date filtering
        'is_active':['exact'],
    }

    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [AccountPermission]

    def get_permissions(self):
        if self.action == 'list':
           
            # Only allow authenticated users to list users
            return [IsAuthenticated()]
        else:
            # For other actions, no authentication is required
            return []
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CustomUserSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        user = self.request.user
        
        queryset = cache.get('Users')      
        if queryset is None:
            queryset = CustomUser.objects.all()
            cache.set('Users', queryset, cache_time)
        else:
            queryset = queryset   
    
        if not user.is_authenticated:
            # Return an empty queryset or a default response
            query = CustomUser.objects.none()
        elif user.role == roles.SMU:  
            # query = queryset.objects.all()   
            query = queryset 
        elif user.role == roles.SUPERADMIN:
            # query = CustomUser.objects.all()    
            query = queryset       
        elif user.role == roles.ADMIN:
            # Regular user can see SampleForm instances with form_available='user'
            # query = CustomUser.objects.filter(is_active = True)    
            query = queryset.filter(is_active = True)
        elif user.role == roles.SUPERVISOR:
            # Regular user can see SampleForm instances with form_available='user'
            # query = CustomUser.objects.filter(is_active = True).filter(Q(role=roles.ANALYST) | Q(email = user.email))   
            query = queryset.filter(is_active = True).filter(Q(role=roles.ANALYST) | Q(email = user.email))
        elif user.role == roles.VERIFIER:
            # Regular user can see SampleForm instances with form_available='user'
            # query = CustomUser.objects.filter(is_active = True).filter(role=roles.USER)   
            query = queryset.filter(is_active = True).filter(role=roles.USER)      
        else:
            # query = CustomUser.objects.filter(email=user.email,is_active = True)
            query = queryset.filter(email=user.email,is_active = True)
            # raise PermissionDenied("You do not have permission to access this resource.")
        return query.order_by("-created_date")
     
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response(data)
    
    def retrieve(self, request, pk=None):
        try:
            cache_key = f'user_{pk}'
            cached_data = cache.get(cache_key)

            if cached_data is None:
                queryset = self.get_queryset()  # Call get_queryset to retrieve the queryset
                user = queryset.get(pk=pk)  # Retrieve the user from the queryset
                # Use the serializer class associated with the viewset
                serializer = self.get_serializer(user)
                data = serializer.data
                cache.set(cache_key , data, cache_time)
            else:
                data = cached_data

            return Response(data)
        except:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

     
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "User Account created successfully",
            "data": serializer.data
        }

        name = request.POST.getlist('images[name]')
        files =  request.FILES.getlist('images[file]')

        custom_user_detail = CeateClientCategoryDetail(name,files,serializer.data['id'],"create")

        #NotificationHandler(serializer.instance,request,'create',"CustomUser")

        cache.delete('Users')
        cache.delete('UsersuserLimitedData')
    
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if 'is_active' not in request.data:
            serializer.validated_data['is_active'] = instance.is_active

        if 'is_email_verified' not in request.data:
            serializer.validated_data['is_email_verified'] = instance.is_email_verified

        # Save the updated object to the database   
        self.perform_update(serializer)

        # Create a custom response
        response_data = {
            "message": "User Account updated successfully",
            "data": serializer.data
        }

        name = request.POST.getlist('images[name]')
        files =  request.FILES.getlist('images[file]')

        custom_user_detail = CeateClientCategoryDetail(name,files,serializer.data['id'],"update")
        
        NotificationHandler(serializer.instance,request,'update','CustomUser')
        # Return the custom response
        cache.delete('Users')
        cache.delete('UsersuserLimitedData')
        
        return Response(response_data)
    
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_active:
            # If the user is active, mark them as inactive
           
            instance.is_active = False
            instance.delete= "delete"
            instance.save()
            # Create a custom response
            response_data = {
                "message": "User Account marked as inactive"
            }
        else:
            # If the user is already inactive, return a custom error response
            response_data = {
                "message": "User Account is already inactive"
            }

        # Return the custom response
        return Response(response_data)




class RoleViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  
    
    def get(self,request,format=None):
        my_tuple = CustomUser.ROLE_CHOICES
        serializer = RoleSerializer(data=my_tuple,many=True)
        serializer.is_valid()
        serialized_data = serializer.data
        # authentication_classes = [JWTAuthentication]
        # permission_classes = [IsAuthenticated]
        return Response({"roles": serialized_data},status=status.HTTP_200_OK)

class DepartmentTypesViewSet(APIView):    
    def get(self,request,format=None):
        my_tuple = department_type.department_code
        serializer = departmentTypeSerializer(data=my_tuple,many=True)
        serializer.is_valid()
        serialized_data = serializer.data
        return Response({"department_types": serialized_data},status=status.HTTP_200_OK)
     

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "Group created successfully",
            "data": serializer.data
        }

        # Return the custom response
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Save the updated object to the database
        self.perform_update(serializer)

        # Create a custom response
        response_data = {
            "message": "Group updated successfully",
            "data": serializer.data
        }

        # Return the custom response
        return Response(response_data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Perform the default delete logic
        self.perform_destroy(instance)

        # Create a custom response
        response_data = {
            "message": "Group deleted successfully"
        }

        # Return the custom response
        return Response(response_data)

    
class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['name','code_name','is_verified']
    ordering_fields = ['id','name']

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]    

class PermissionAllDelete(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  
    def get(self, request, format=None):
        object = Permission.objects.all().delete()
        return Response({'message': 'All permission delete successful'}, status=status.HTTP_200_OK)

class CheckTokenExpireView(APIView): 
    def get(self, request, format=None):
        # Get the token from the request headers or query parameters
        try:
            raw_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        except:
            return Response({'valid': False}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Verify the access token
            access_token = AccessToken(raw_token)
            access_token.verify()

            # If the token is valid and not expired
            return Response({'valid': True}, status=status.HTTP_200_OK)

        except TokenError:
            # If the token is expired or invalid
            return Response({'valid': False}, status=status.HTTP_401_UNAUTHORIZED)

    
# Create your views here.
class LoginView(APIView):
    @csrf_exempt
    def post(self, request):
        username_or_email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user using either username or email
        user = authenticate(request, username=username_or_email, password=password)
        if user is None:
            user = authenticate(request, email=username_or_email, password=password)

        # If the user is authenticated, log them in and generate tokens
        if user is not None:
            if user.is_active == False:
                return Response({'error': 'Your Account is inactive'}, status=status.HTTP_401_UNAUTHORIZED)
            login(request, user)
            refresh = RefreshToken.for_user(user)
            user_obj = CustomUserSerializer(request.user,context={'request': request}) 
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_obj.data,
                'message': 'Login successful',
            }, status=status.HTTP_200_OK)

        # If the user is not authenticated, return an error message
        else:
            from django.db.models import Q
            user_obj = CustomUser.objects.filter(Q(username=username_or_email) | Q(email=username_or_email))
            if user_obj.exists():
                return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'Invalid username/email'}, status=status.HTTP_401_UNAUTHORIZED)

def CeateClientCategoryDetail(names,files,user_id,action):

    image_data = []

    for name, file in zip(names, files):
       dict_data = {
           'user':user_id,
           'name':name,
           'file':file,
       }
       image_data.append(dict_data)
    if len(image_data)>0:        
        image_serializer = CustomUserImageSerializer(many=True,data=image_data)
        image_serializer.is_valid(raise_exception=True)
        image_serializer.save()    
    return True

class userLimitedData(generics.ListAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]


    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','email','username','first_name','last_name','is_verified','phone']
    ordering_fields = ['username','id']
    filterset_fields = {
        'email': ['exact', 'icontains'],
        'username': ['exact'],
        'is_verified': ['exact'],
        'is_reject': ['exact'],
        'role': ['exact'],
        'client_category_id': ['exact'],
        'created_date': ['date__gte', 'date__lte'],  # Date filtering
        'is_active':['exact'],
    }
    
    def get_queryset(self):
        users = CustomUser.objects.filter(role = roles.USER,is_active = True)
        return users

    def get_serializer_class(self):
        return CustomUserReadLimitedSerializer
    
    def list(self, request, *args, **kwargs):
        # Try to get cached data
        cached_data = cache.get('UsersuserLimitedData')

        if cached_data is None:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

            # Store data in the cache for 5 minutes (300 seconds)
            cache.set('UsersuserLimitedData', data, cache_time)
        else:
            data = cached_data        
        return Response(data)
    
class userAdminLevelData(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','email','username','first_name','last_name','is_verified','phone']
    ordering_fields = ['username','id']
    filterset_fields = {
        'email': ['exact', 'icontains'],
        'username': ['exact'],
        'is_verified': ['exact'],
        'is_reject': ['exact'],
        'role': ['exact'],
        'client_category_id': ['exact'],
        'created_date': ['date__gte', 'date__lte'],  # Date filtering
        'is_active':['exact'],
    }
    
    def get_queryset(self):
        users = CustomUser.objects.filter(Q(role=roles.ANALYST) | Q(role = roles.SUPERVISOR) | Q(role = roles.VERIFIER) | Q(role = roles.ADMIN) | Q(role = roles.SUPERADMIN))
        return users

    def get_serializer_class(self):
        return userAdminLevelDataSerializer
    
    def list(self, request, *args, **kwargs):
        # Try to get cached data
        cached_data = cache.get('UsersuserLimitedData')

        if cached_data is None:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

            # Store data in the cache for 5 minutes (300 seconds)
            cache.set('UsersuserLimitedData', data, cache_time)
        else:
            data = cached_data        
        return Response(data)
    
   
    

             