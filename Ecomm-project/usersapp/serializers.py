from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from .models import CustomizeUser
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import Customer, Seller, Address


class RegisterSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=queryset)]
    )

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=queryset)]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }


class LoginSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()

    def validate(self, attrs):

        if User.objects.filter(username=attrs['username']).exists():
            user = User.objects.get(username=attrs['username'])
            customize = CustomizeUser.objects.filter(user=user.pk).first()
            if not check_password(attrs['password'], user.password):
                customize = CustomizeUser.objects.filter(user=user.pk).first()
                customize.invalid_password_attempt = customize.invalid_password_attempt + 1
                customize.save()
                max_attempts = 5

                if customize.invalid_password_attempt >= max_attempts:
                    customize.is_locked = True
                    customize.save()

                raise serializers.ValidationError({
                    'error': 'wrong password!!'
                })
            if user.is_active == False:
                raise serializers.ValidationError({
                    'error': 'Your account is not active!! please activate your account first.'
                })
            if customize.is_locked == True:
                raise serializers.ValidationError({
                    'error': 'Your Account is locked due to too many password attempts..!!Unlock your account throught reset password!.'
                })
        else:
            raise serializers.ValidationError({
                'error': 'user not found'
            })
        return attrs

    class Meta:
        model = User
        fields = ['username', 'password']


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(max_length=15)
    new_password = serializers.CharField(max_length=15)
    confirm_password = serializers.CharField(max_length=15)

    def validate(self, attrs):
        user = self.context.get('user')
        user = User.objects.get(username=user.username)
        if not check_password(attrs['old_password'], user.password):
            raise serializers.ValidationError({
                'error': 'old password is Wrong!!'
            })
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError({
                'error': 'new & old password can not be same'
            })
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'error': 'password does not match'
            })
        user.set_password(attrs['new_password'])
        user.save()

        return attrs


class PasswordResetSerializer(serializers.Serializer):

    email = serializers.EmailField(
        required=True
    )

    class Meta:
        model = User
        fields = ('email')


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        min_length=4
    )

    def validate(self, data):
        password = data.get('password')
        token = self.context.get('kwargs').get('token')
        encoded_pk = self.context.get('kwargs').get('encoded_pk')

        if token is None or encoded_pk is None:
            raise serializers.ValidationError({
                'error': 'missing data'
            })
        pk = urlsafe_base64_decode(encoded_pk).decode()
        try:
            user = User.objects.get(pk=pk)
        except:
            raise serializers.ValidationError({
                'error': 'Your uid is Wrong'
            })
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError({
                'error': 'reset token is invalid'
            })
        user.set_password(password)
        user.is_active = True
        customizeuser = CustomizeUser.objects.get(user=user)
        customizeuser.invalid_password_attempt = 0
        customizeuser.is_locked = False
        customizeuser.save()
        user.save()
        return data

    class Meta:
        fields = ('password')

# customer serializer


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'
        depth = 1

# sellers serializer


class SellerSerialzier(serializers.ModelSerializer):
    queryset = Seller.objects.all()

    gst = serializers.IntegerField(
        required=True,
        validators=[UniqueValidator(queryset=queryset)]
    )

    company_contact = serializers.IntegerField(
        required=True,
        validators=[UniqueValidator(queryset=queryset)]
    )

    company_name = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=queryset)]
    )

    class Meta:
        model = Seller
        fields = '__all__'
        depth = 1

# address serializer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['city', 'state', 'address_line', 'zip_code', 'label']


# admin serializer
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']
