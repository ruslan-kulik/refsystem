import time
import random
from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render, redirect
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import OTPCode, CustomUser
from .forms import CustomUserCreationForm, ActivateInviteForm
from .serializers import (
    PhoneSerializer, VerifyOTPSerializer,
    ProfileSerializer, ActivateInviteSerializer
)
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        return render(request, self.template_name, {'form': CustomUserCreationForm()})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Если введен чужой код — привязываем пригласившего
            code = form.cleaned_data.get('invite_code_input')
            if code:
                try:
                    inviter = CustomUser.objects.get(invite_code=code)
                    user.invited_by = inviter
                except ObjectDoesNotExist:
                    form.add_error('invite_code_input', 'Неверный invite-код')
                    return render(request, self.template_name, {'form': form})
            user.save()
            # аутентификация и редирект
            phone = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password1')
            authenticated_user = authenticate(request, phone_number=phone, password=password)
            if authenticated_user:
                login(request, authenticated_user)
            return redirect('home')

class SendOTPView(generics.GenericAPIView):
    serializer_class = PhoneSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone_number']

        time.sleep(random.uniform(1, 2))  # Симуляция задержки

        code = f"{random.randint(0, 9999):04d}"
        OTPCode.objects.create(phone_number=phone, code=code)

        return Response({'detail': 'Код отправлен'}, status=status.HTTP_200_OK)


class VerifyOTPView(generics.GenericAPIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)

        phone = s.validated_data['phone_number']
        code = s.validated_data['code']

        otp = OTPCode.objects.filter(
            phone_number=phone, code=code, is_used=False
        ).order_by('-created_at').first()

        if not otp:
            return Response({'detail': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)

        otp.is_used = True
        otp.save()

        user, _ = CustomUser.objects.get_or_create(phone_number=phone)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

        invite_code = request.data.get('invite_code', None)
        user, created = CustomUser.objects.get_or_create(phone_number=phone)
        if created and invite_code:
            try:
                inviter = CustomUser.objects.get(invite_code=invite_code)
                user.invited_by = inviter
                user.save()
            except CustomUser.DoesNotExist:
                pass


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ActivateInviteSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)

    def validate_invite_code(self, value):
        try:
            inviter = CustomUser.objects.get(invite_code=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('Неверный код')
        return value

class ActivateInviteView(generics.GenericAPIView):
    serializer_class = ActivateInviteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['invite_code']
        user = request.user

        if user.invited_by:
            return Response(
                {'detail': 'Код уже активирован'},
                status=status.HTTP_400_BAD_REQUEST
            )

        inviter = CustomUser.objects.get(invite_code=code)
        user.invited_by = inviter
        user.save()

        return Response({'detail': 'Код активирован'}, status=status.HTTP_200_OK)

class ActivateInviteWebView(View):
    template_name = 'users/activate_invite.html'

    def get(self, request):
        form = ActivateInviteForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ActivateInviteForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['invite_code']
            if request.user.invited_by:
                form.add_error(None, 'Код уже активирован')
            else:
                try:
                    inviter = CustomUser.objects.get(invite_code=code)
                    request.user.invited_by = inviter
                    request.user.save()
                    return redirect('users:profile')
                except CustomUser.DoesNotExist:
                    form.add_error('invite_code', 'Неверный код')
        return render(request, self.template_name, {'form': form})