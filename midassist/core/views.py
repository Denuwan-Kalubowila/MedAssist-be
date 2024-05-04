"""
This is the view of core module
"""
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post, User, Doctor
from .serializers import PostSerializer, DoctorSerializer,MessageSerializer
from .serializers import UserSerializer
from .chat import get_response_medassist

user_id = 0


@api_view(['POST'])
@csrf_exempt
def login_view(request):
    """
        this method use for login
    """
    global user_id

    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()

    if user:
        if user.password == password:
            user_id = user.id
            print(user_id)
            return Response({'message': 'Login successful', 'user_id': user_id}, status=200)
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
    global user_id
    user_id = 0
    print(user_id)
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


@api_view(['GET'])
def user_details(request):
    """
    Retrieve details of the logged-in user
    """
    global user_id
    print(user_id)
    if user_id:
        user = User.objects.filter(id=user_id).first()
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({'error': 'User not found'}, status=404)
    else:
        return Response({'error': 'User session not found'}, status=404)


@api_view(['GET'])
def get_image(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def post_image(request):
    posts_serializer = PostSerializer(data=request.data)
    if posts_serializer.is_valid():
        posts_serializer.save()
        return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
    else:
        print('error', posts_serializer.errors)
        return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def doctors_view(request):
    doctors = Doctor.objects.all()  # Retrieve all doctors from the database
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def chat(request):
    user_msg_serializer = MessageSerializer(data=request.data)
    if user_msg_serializer.is_valid():
        user_msg = user_msg_serializer.data['message']  # Assuming 'message' field in serializer
        response = get_response_medassist(user_msg)
        return Response(response)
    else:
        print('Error:', user_msg_serializer.errors)
        return Response(user_msg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)