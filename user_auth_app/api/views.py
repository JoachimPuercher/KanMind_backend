from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(['POST'])
@permission_classes([AllowAny])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        new_user = serializer.save()
        token, create = Token.objects.get_or_create(user=new_user)
        data = {
            'token' : token.key,
            'username' : new_user.username,
            'email' : new_user.email
        }
        
    else:
        data=serializer.errors
        
    return Response(data)