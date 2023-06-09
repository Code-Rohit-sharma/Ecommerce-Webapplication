from django.shortcuts import render
from .serializers import RegisterSerializer, ChangePasswordSerializer, LoginSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer, CustomerSerializer, SellerSerialzier, AddressSerializer, AdminSerializer
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
from .models import Role, UserRole, Customer, Seller, Address, CustomizeUser
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
from Ecommerce.models import Product

# cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
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
        CustomizeUser.objects.create(
            user=user, is_deleted=False, is_expired=False, is_locked=False, invalid_password_attempt=0)
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


class DeleteUserView(APIView):
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

        if not check_password(data['password'], user.password):
            return Response({
                'message': 'password not found',
                'status': status.HTTP_401_UNAUTHORIZED
            })

        user.is_active = False
        customize_user = CustomizeUser.objects.get(user=user)
        customize_user.is_deleted = True
        user.save()
        customize_user.save()

        return Response({
            'message': 'user deleted',
            'status': status.HTTP_200_OK
        })


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
        customizeuser = CustomizeUser.objects.get(user=user)

        if not check_password(password, user.password):
            customizeuser.invalid_password_attempt = customizeuser.invalid_password_attempt + 1
            customizeuser.save()
            if customizeuser.invalid_password_attempt >= 5:
                customizeuser.is_locked = True
                customizeuser.save()

            return Response({
                'message': 'Invalid Credentials',
                'status': status.HTTP_400_BAD_REQUEST
            })

        if customizeuser.is_locked == True:
            return Response({
                'message': 'Your accout is locked due to too many wrong password attempts unlock account from reset password',
                'status': status.HTTP_401_UNAUTHORIZED
            })

        if customizeuser.is_deleted == True:
            return Response({
                'message': 'This is account is already deleted',
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


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, format=None):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)

            return Response({'msg': 'logout successfully'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': 'error'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        data = request.data
        user = request.user
        serializer = ChangePasswordSerializer(
            data=data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        customizeuser = CustomizeUser.objects.get(user=user)
        customizeuser.password_update_date = datetime.now()
        customizeuser.save()

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
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
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

    @method_decorator(cache_page(60*60*1))
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

    @method_decorator(cache_page(60*60*1))
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
                'message': 'seller not found',
                'status': status.HTTP_401_UNAUTHORIZED
            })

        serializer = SellerSerialzier(user, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
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


class AdminView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = User.objects.filter(is_superuser=True)
        serializer = AdminSerializer(user, many=True)
        return Response({
            'data': serializer.data,
            'status': status.HTTP_200_OK
        })

    def patch(self, request):
        data = request.data
        user = request.user
        try:
            user = User.objects.get(username=user)
        except:
            return Response({
                'error': 'user not found',
                'status': status.HTTP_400_BAD_REQUEST
            })
        if not user.is_superuser == True:
            return Response({
                'error': 'you are not a super user',
                'status': status.HTTP_401_UNAUTHORIZED
            })
        serializer = AdminSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'user updated',
            'status': status.HTTP_200_OK
        })


class AdminRegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data['username']
        try:
            user = User.objects.get(username=username)
            if user:
                return Response({
                    'error': 'username already taken'
                })
        except:
            serializer = AdminSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            try:
                user = User.objects.get(username=username)
            except:
                return Response({
                    'error': 'username not found'
                })
            user.is_superuser = True
            user.is_staff = True
            user.save()

        return Response({
            'message': 'admin registered',
            'status': status.HTTP_200_OK
        })


class ProductActivation(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request):
        data = request.data
        user = request.user
        activation_status = data['activation_status']
        try:
            user = User.objects.get(username=user)
        except:
            return Response({
                'error': 'user not found'
            })

        if user.is_superuser == True:
            try:
                product = Product.objects.get(pk=data['product_id'])
            except:
                return Response({
                    'error': 'product not found'
                })

            product.is_active = activation_status
            product.save()
        else:
            return Response({
                'error': 'you are not a super user'
            })

        return Response({
            'message': f'product active status changed to {activation_status}',
            'status': status.HTTP_200_OK
        })
