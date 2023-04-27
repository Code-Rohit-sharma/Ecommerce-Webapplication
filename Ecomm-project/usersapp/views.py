from django.shortcuts import render
from .serializers import RegisterSerializer, ChangePasswordSerializer, LoginSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer, CustomerSerializer, SellerSerialzier, AddressSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from .generate_token import get_tokens_for_user
from django.utils.encoding import force_bytes, smart_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tasks import send_mail_password_reset, send_mail_activation_link
from django.contrib.auth.hashers import check_password
from .models import Role, UserRole, Customer, Seller, Address

# Create your views here.


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = User.objects.all()
        serializer = RegisterSerializer(users, many=True)
        return Response({
            'data': serializer.data
        })

    def post(self, request):
        data = request.data
        # contact = request.data['contact']
        serializer_class = RegisterSerializer(data=data)
        serializer_class.is_valid(raise_exception=True)
        user = serializer_class.save()
        user.set_password(user.password)
        user.is_active = False
        user.save()
        custId = user.pk
        encodedCustId = urlsafe_base64_encode(force_bytes(custId))
        token = PasswordResetTokenGenerator().make_token(user)
        activation_link = 'http://127.0.0.1:8000/users/confirm-registration/' + \
            encodedCustId+'/'+token+'/'
        # customer = Customer.objects.get_or_create(user = user,contact = contact)
        send_mail_activation_link.delay(user.email, activation_link)

        return Response({
            'acitvation_link': activation_link,
            'message': 'user register successfully',
            'status': status.HTTP_200_OK
        })


class ConfirmRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, encoded_pk, token, format=None):
        id = smart_str(urlsafe_base64_decode(encoded_pk))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"Error": "Token is not valid or expired"})
        user.is_active = True
        user.save()
        token = get_tokens_for_user(user)
        role = Role.objects.get(authority='CUSTOMER')
        userRole = UserRole.objects.get_or_create(user=user, role=role)
        return Response({
            "data": "Your Account activated "+user.username, "jwt-token": token},
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        try:
            user = User.objects.get(username=username)
        except:
            return Response({
                'message': 'Invalid Credentials',
                'status': status.HTTP_400_BAD_REQUEST
            })
        if not check_password(password, user.password):
            return Response({
                'message': 'Invalid Credentials',
                'status': status.HTTP_400_BAD_REQUEST
            })

        if not user.is_active:
            custId = user.pk
            encodedCustId = urlsafe_base64_encode(force_bytes(custId))
            token = PasswordResetTokenGenerator().make_token(user)
            activation_link = 'http://127.0.0.1:8000/users/confirm-registration/' + \
                encodedCustId+'/'+token+'/'
            send_mail_activation_link.delay(user.email, activation_link)
            return Response({
                'message': 'Your account is not Active please Activate your account!please check your Email & click on Activate your account',
                'status': status.HTTP_400_BAD_REQUEST
            })

        token = get_tokens_for_user(user)
        return Response({
            'token': token,
            'message': 'successfully Login',
            'status': status.HTTP_200_OK
        })


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        data = request.data
        user = request.user
        serializer = ChangePasswordSerializer(
            data=data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        return Response({
            'message': 'password updated successfully!!',
            'status': status.HTTP_200_OK
        })


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer_class = PasswordResetSerializer(data=data)
        serializer_class.is_valid(raise_exception=True)
        email = serializer_class.data['email']
        # user = User.objects.filter(email = email).first()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExists:
            return Response({
                'message': 'User Does not Exist'
            })

        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        reset_url = reverse(
            "reset-password",
            kwargs={'encoded_pk': encoded_pk, 'token': token}
        )

        reset_link = 'http://127.0.0.1:8000/users/password-reset/'+encoded_pk+'/'+token+'/'
        send_mail_password_reset.delay(email, reset_link)
        return Response({
            'message': f'your password reset link {reset_link}',
            'status': status.HTTP_200_OK
        })


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, *args, **kwargs):
        data = request.data
        serializer_class = PasswordResetConfirmSerializer(
            data=data, context={'kwargs': kwargs})
        serializer_class.is_valid(raise_exception=True)
        return Response({
            'message': 'password reset complete',
            'status': status.HTTP_200_OK
        })

# Customer views


class CustomerView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response({
            'data': serializer.data
        })

    def post(self, reqeust):
        data = reqeust.data
        user = reqeust.user
        try:
            user = User.objects.get(username=user.username)
        except:
            return Response({
                'message': 'user not found'
            })

        serializer = CustomerSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            customer = Customer.objects.create(
                user=user, contact=serializer.data['contact'], alternate_contact=serializer.data['alternate_contact'])

        return Response({
            'message': 'Customer Contact Saved',
            'status': status.HTTP_200_OK
        })

    def patch(self, request):
        data = request.data
        user = request.user
        try:
            user = Customer.objects.get(user=user)
        except:
            return Response({
                'message': 'user not found'
            })

        serializer = CustomerSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()

        return Response({
            'message': 'contact updated successfully',
            'status': status.HTTP_200_OK
        })

# sellers views


class SellerView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        sellers = Seller.objects.all()
        serializer = SellerSerialzier(sellers, many=True)
        return Response({
            'data': serializer.data
        })

    def post(self, request):
        data = request.data
        user = request.user
        gst = data['gst']
        company_contact = data['company_contact']
        company_name = data['company_name']
        try:
            user = User.objects.get(username=user.username)
        except:
            return Response({
                'message': 'user not found'
            })

        serializer = SellerSerialzier(data=data)
        if serializer.is_valid(raise_exception=True):
            seller = Seller.objects.create(
                user=user, gst=gst, company_contact=company_contact, company_name=company_name)
            serializer.save()

        return Response({
            'message': 'you are registered as a seller',
            'status': status.HTTP_200_OK
        })

    def patch(self, request):
        data = request.data
        user = request.user

        try:
            user = Seller.objects.get(user=user)
        except:
            return Response({
                'message': 'user not found',
                'status': status.HTTP_401_UNAUTHORIZED
            })

        serializer = SellerSerialzier(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response({
            'msg': 'data Updated',
            'status': status.HTTP_200_OK
        })


class AddressView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        data = request.data
        user = request.user

        try:
            user = User.objects.get(username=user.username)
        except:
            return Response({
                'message': 'user not found',
                'status': status.HTTP_400_BAD_REQUEST
            })
        serializer = AddressSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            address = Address.objects.create(user=user, **serializer.data)

        return Response({
            'message': 'address saved',
            'status': status.HTTP_200_OK
        })

    def patch(self, request):
        data = request.data
        user = request.user
        label = data['label']
        try:
            user = Address.objects.filter(user=user).get(label=label)
        except:
            return Response({
                'message': 'user address not found',
                'status': status.HTTP_400_BAD_REQUEST
            })

        serializer = AddressSerializer(user, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response({
            'message': 'address updated',
            'status': status.HTTP_200_OK
        })