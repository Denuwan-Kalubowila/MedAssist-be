"""
This is the view of core module
"""
import os
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .CheXNet_model import predict_chexnet
from .brain_tumor_model import predict
from rest_framework.request import Request
from .models import Image, User, Doctor, Message, ChexnetImage
from .serializers import ImageSerializer, PdfSerializer, MessageSerializer, CheXNet_ImageSerializer
from .serializers import UserSerializer, DoctorSerializer
from .extract_text import extract_text_from_pdf
from requests.exceptions import ConnectionError
import requests
from .gemini_api import model
from dotenv import load_dotenv
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

load_dotenv()

# from .chat import get_response_medassist

user_id = 0

@api_view(['POST'])
def login_view(request):
    """
    Login and return JWT tokens
    """
    email = request.data.get('email')
    password = request.data.get('password')

    # Authenticate user
    user = authenticate(request, email=email, password=password)
    if user:
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_view(request):
    """
    Logout and blacklist the user's refresh token
    """
    try:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'success': 'Logged out successfully'}, status=200)
    except Exception as e:
        return Response({'error': 'Invalid token'}, status=400)

@api_view(['POST'])
def signup_view(request):
    """
    Signup and create a new user
    """
    email = request.data.get('email')
    user_check = User.objects.filter(email=email).first()
    # print(user_check)
    if user_check:
        return Response({'detail': 'Email is already exist'}, status=400)
    else:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                user.set_password(request.data['password'])  # Hash password
                user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#no need this api now
@api_view(['GET'])
def user_details(request):
    """
    Retrieve details of the logged-in user
    """
    global user_id
    # print(user_id)
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
        image_path = posts_serializer.instance.image.path
        predicted_class = predict(image_path)
        if predicted_class == 0:
            p_name = "glioma"
        elif predicted_class == 1:
            p_name = "meningioma"
        elif predicted_class == 2:
            p_name = "notumor"
        elif predicted_class == 3:
            p_name = "pituitary"
        response_data = {
            'image': posts_serializer.data,
            'predicted_class': p_name
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        # print('error', posts_serializer.errors)
        return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def post_pdf(request):
    if request.method == 'POST':
        pdf_file = request.data.get('pdf_file')
        user = request.data.get('user')

        pdf_text = extract_text_from_pdf(pdf_file)

        try:
            # Use the generative AI model to generate a response
            convo = model.start_chat(history=[])
            message = pdf_text  # Pass the extracted text as input
            convo.send_message(message)
            response = convo.last.text
            # print(response)

            post_data = {'pdf_file': pdf_file, 'user': user}
            post_serializer = PdfSerializer(data=post_data)

            if post_serializer.is_valid():
                post_serializer.save()
                return Response({"pdf_data": post_serializer.data, "response": response},
                                status=status.HTTP_201_CREATED)
            else:
                return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ConnectionError:
            # Handle internet connection error
            return Response({"message": "Internet connection error. Please try again later."},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            # Handle other errors
            # print("Error:", e)
            return Response({"message": "An error occurred while processing your request."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def post_doctor(request):
    """
    This method is used to post a doctor
    """
    doctor_serializer = DoctorSerializer(data=request.data)
    if doctor_serializer.is_valid():
        doctor_serializer.save()
        return Response(doctor_serializer.data, status=status.HTTP_201_CREATED)
    else:
        # print('error', doctor_serializer.errors)
        return Response(doctor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def doctors_view(request):
    """
    This method is used to retrieve all doctors from the database
    """
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_doctotrs_by_review(request):
    """
    This method is used to retrieve all doctors from the database
    """
    doctors = Doctor.objects.all().order_by('reviews')[:10]
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
                    return Response({"error": "The response did not contain an answer."},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"error": "Failed to get a valid response from the service."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as e:
            # print('Error:', e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        # print('Error:', user_msg_serializer.errors)
        return Response(user_msg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def post_chexnet_image(request):
    serializer = CheXNet_ImageSerializer(data=request.data)
    if serializer.is_valid():
        image_instance = serializer.save()

        image_path = image_instance.image.path

        try:
            predicted_class = predict_chexnet(image_path)

            # Map the predicted class to a label
            class_labels = {
                0: "NORMAL",
                1: "PNEUMONIA"
            }

            # Get the label or use "UNKNOWN" if the class is not recognized
            predicted_label = class_labels.get(predicted_class, "UNKNOWN")

            return Response({
                'image': CheXNet_ImageSerializer(image_instance).data,
                'predicted_class': predicted_label
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

