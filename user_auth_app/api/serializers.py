from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import UserProfile

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField()

    class Meta:
        model = User
        fields = ["fullname", "email", "password", "repeated_password"]
        extra_kwargs = {
            'password' : {
                'write_only' : True
            }
        }

    def save(self):
        password = self.validated_data['password']
           
        user = User(email=self.validated_data["email"], username=self.validated_data["email"])
        user.set_password(password)
        user.save()
        UserProfile.objects.create(
            user=user,
            fullname=self.validated_data["fullname"],
            data_save_accepted=True
        )
        return user
        
    def validate_email(self, value):
        new_mail = value.lower()
        if User.objects.filter(email=new_mail).exists():
            raise serializers.ValidationError("Email already exists")
        return new_mail
    
    def validate_data_accepted(self, value):
        if (value==True):
            return value
        else:
            raise serializers.ValidationError("Privacy Policy not accepted")

    def validate(self, values):
        if values["password"] != values["repeated_password"]:
            raise serializers.ValidationError("Passwords do not match!")
        else:
            return values
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, values):
        user = User.objects.filter(email=values["email"]).first()

        if user:
            pw_valid = user.check_password(values["password"])

            if pw_valid == True:
                values["user"] = user
                return values
            else:
                raise serializers.ValidationError("Invalid credentials.")
            
        else:
            raise serializers.ValidationError("Invalid credentials.")


class EmailQuerySerializer(serializers.Serializer):
    email = serializers.EmailField()