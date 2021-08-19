from django.contrib.auth import authenticate
from rest_framework import serializers
from account.models import MyUser
from account.utils import send_activation_code


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=6, write_only=True)
    password_confirm = serializers.CharField(max_length=6, write_only=True)

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, validate_data):
        password = validate_data.get('password')
        password_confirm = validate_data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Password do not match')
        return validate_data

    def create(self, validate_data):
        email = validate_data.get('email')
        password = validate_data.get('password')
        user = MyUser.objects.create_user(email=email, password=password)
        send_activation_code(email=user.email, activation_code=user.activation_code)
        return user
    # """This function is called when self.save() method is called """


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                message = 'Unable to login in with provided credentials'
                raise serializers.ValidationError(message, code="authorization")

        else:
            message = "Must include 'email' and 'password'."
            raise serializers.ValidationError(message, code="authorization")

        attrs['user'] = user
        return attrs