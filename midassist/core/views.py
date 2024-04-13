"""
This is the view of core module
"""
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import User

@api_view(['POST'])
@csrf_exempt
def login_view(request):
    """
        this method use for login
    """
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()

    if user:
        if user.password == password:
            return Response({'message': 'Login successful'}, status=200)
        else:
            return Response({'error': 'Incorrect password'}, status=401)
    else:
        return Response({'error': 'Email not found'}, status=404)


@api_view(['POST'])
@csrf_exempt
def logout_view(request):
    """
        this method use for logout
    """
    logout(request)
    return Response({'success': 'Logged out successfully'})


@api_view(['POST'])
@csrf_exempt
def signup_view(request):
    """
        this method use for Signup
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
