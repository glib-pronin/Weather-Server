from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth import authenticate 
from .serializers import *
from .utils import *

# Create your views here.

class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            code = generate_code()
            verification = EmailVerification.objects.create(user=user)
            verification.set_code(code)
            send_verification_mail_async(user.email, code)
            return Response({'success': True})
        return Response({'success': False, 'errors': serializer.errors}, status=400)
    
class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request=request, username=username, password=password)
        if not user:
            return Response({'success': False, 'errors': 'wrong credentials'}, status=401)
        if not hasattr(user, 'email_verification'):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        
        verification = user.email_verification
        code = generate_code()
        verification.set_code(code)
        send_verification_mail_async(user.email, code)
        return Response({'success': False, 'errors': 'not verified email'}, status=403)
    
class VerifyEmailAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        try:
            user = User.objects.get(email=email)
            verification = user.email_verification
        except:
            return Response({'success': False, 'errors': 'bad request'}, status=400)
        if not verification.check_code(code):
            return Response({'success': False, 'errors': 'wrong or expired code'}, status=400)
        verification.delete()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    
class MeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = MeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    