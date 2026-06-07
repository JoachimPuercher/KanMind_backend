from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer, LoginSerializer, EmailQuerySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from rest_framework import status
from ..models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        new_user = serializer.save()
        token, create = Token.objects.get_or_create(user=new_user)
        data = {
            'token' : token.key,
            'fullname' : new_user.userprofile.fullname,
            'email' : new_user.email,
            'user_id' : new_user.pk
        }

        return Response(data, status=status.HTTP_201_CREATED)
        
    else:
        data=serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        login_user = serializer.validated_data["user"]
        token, create = Token.objects.get_or_create(user=login_user)
        data = {
            'token' : token.key,
            'fullname' : login_user.userprofile.fullname,
            'email' : login_user.email,
            'user_id' : login_user.pk
        }

        return Response(data, status=status.HTTP_200_OK)
        
    else:
        data=serializer.errors
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    

@api_view(['GET'])
def email_check_view(request):
    param_email = request.query_params.get("email").lower()
    query_serializer = EmailQuerySerializer(data={"email" : param_email})
    if query_serializer.is_valid():
        user = User.objects.filter(email=param_email).first()

        if user is None:
            return Response ({"error" : "User not found"},status=status.HTTP_404_NOT_FOUND)
        
        data = {
            "id" : user.id,
            "email" : user.email,
            "fullname" : user.userprofile.fullname
        }
        return Response (data, status=status.HTTP_200_OK)
    
    else:
        return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)