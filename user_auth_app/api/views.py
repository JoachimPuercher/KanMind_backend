from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status


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
        
    else:
        data=serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    return Response(data, status=status.HTTP_201_CREATED)