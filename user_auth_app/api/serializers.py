from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(write_only=True)
    

    class Meta:
        model = User
        fields = ["username", "email", "password", "repeat_password"]
        extra_kwargs = {
            'password' : {
                'write_only' : True
            }
        }

    def save(self):
        password = self.validated_data['password']
        repeat_password = self.validated_data['repeat_password']

        if (password != repeat_password):
            raise serializers.ValidationError({"error" : "Passwords do not match!"})
            
        user = User(email=self.validated_data["email"], username=self.validated_data["username"])
        user.set_password(password)
        user.save()
        return user
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"error" : "Email already exists"})
        return value
        
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError({"error" : "Username already exists"})
        return value