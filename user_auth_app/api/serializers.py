from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import UserProfile

class RegistrationSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField()
    data_accepted = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = ["fullname", "email", "password", "repeat_password", "data_accepted"]
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
            data_save_accepted=self.validated_data["data_accepted"]
        )
        return user
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate_data_accepted(self, value):
        if (value==True):
            return value
        else:
            raise serializers.ValidationError("Privacy Policy not accepted")

    def validate(self, values):
        if values["password"] != values["repeat_password"]:
            raise serializers.ValidationError("Passwords do not match!")
        else:
            return values