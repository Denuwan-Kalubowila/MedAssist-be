"""
This is the view of core module
"""
import os
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Image, User, Doctor,Message
from .serializers import ImageSerializer, PdfSerializer,MessageSerializer
from .serializers import UserSerializer, DoctorSerializer
from .extract_text import extract_text_from_pdf
from requests.exceptions import ConnectionError
import requests
from dotenv import load_dotenv

load_dotenv()

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
    """
    This method is used to retrieve all images from the database
    """
    posts = Image.objects.all()
    serializer = ImageSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def post_image(request):
    """
    This method is used to post an image file
    """
    posts_serializer = ImageSerializer(data=request.data)
    if posts_serializer.is_valid():
        posts_serializer.save()
        return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
    else:
        print('error', posts_serializer.errors)
        return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def post_pdf(request):
    """
    This method is used to post a pdf file and get a response GEMINI model
    """
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')
        user = "1"
        pdf_text = extract_text_from_pdf(pdf_file)

        try:
            convo = model.start_chat(history=[])
            message = pdf_text
            convo.send_message(message)
            response = convo.last.text
            print(response)

            post_data = {'pdf_file': pdf_file, 'user': user}
            post_serializer = PdfSerializer(data=post_data)

            if post_serializer.is_valid():
                post_serializer.save()
                return Response({"pdf_data": post_serializer.data, "response": response}, status=status.HTTP_201_CREATED)
            else:
                return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ConnectionError:
            return Response({"message": "Internet connection error. Please try again later."},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            print("Error:", e)
            return Response({"message": "An error occurred while processing your request."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def doctors_view(request):
    """
    This method is used to retrieve all doctors from the database
    """
    doctors = Doctor.objects.all()  # Retrieve all doctors from the database
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def chat(request):
    """
    This method is used to chat with the bot
    params:request(user message)
    return: response(bot message)
    """
    user_msg_serializer = MessageSerializer(data=request.data)
    if user_msg_serializer.is_valid():
        user_msg = user_msg_serializer.validated_data['message']
        print(user_msg)
        payload = {
            "question": user_msg
        }
        try:
            response = requests.post(os.getenv('CLOUD_RUN_URL'), json=payload)    
            if response.status_code == 200:
                response_data = response.json()
                if 'answer' in response_data:
                    message_instance = Message.objects.create(
                        message=user_msg,
                        bot_response=response_data['answer'],
                        user=user_msg_serializer.validated_data['user']
                    )
                    return Response({"answer": response_data['answer']}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "The response did not contain an answer."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"error": "Failed to get a valid response from the service."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
    else:
        print('Error:', user_msg_serializer.errors)
        return Response(user_msg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)