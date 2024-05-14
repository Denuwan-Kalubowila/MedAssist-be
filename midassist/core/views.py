"""
This is the view of core module
"""
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .extract_text import extract_text_from_pdf
from .models import Image, User, Doctor
from .serializers import ImageSerializer, PdfSerializer, MessageSerializer
from .serializers import UserSerializer, DoctorSerializer
from .gemini_api import model
from requests.exceptions import ConnectionError

# from .chat import get_response_medassist

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
    posts = Image.objects.all()
    serializer = ImageSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def post_image(request):
    posts_serializer = ImageSerializer(data=request.data)
    if posts_serializer.is_valid():
        posts_serializer.save()
        return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
    else:
        print('error', posts_serializer.errors)
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
            print(response)

            post_data = {'pdf_file': pdf_file, 'user': user}
            post_serializer = PdfSerializer(data=post_data)

            if post_serializer.is_valid():
                post_serializer.save()
                return Response({"pdf_data": post_serializer.data, "response": response}, status=status.HTTP_201_CREATED)
            else:
                return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ConnectionError:
            # Handle internet connection error
            return Response({"message": "Internet connection error. Please try again later."},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            # Handle other errors
            print("Error:", e)
            return Response({"message": "An error occurred while processing your request."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def doctors_view(request):
    doctors = Doctor.objects.all()  # Retrieve all doctors from the database
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


"""@api_view(['POST'])
def chat(request):
    user_msg_serializer = MessageSerializer(data=request.data)
    if user_msg_serializer.is_valid():
        user_msg = user_msg_serializer.data['message']  # Assuming 'message' field in serializer
        response = get_response_medassist(user_msg)
        return Response(response)
    else:
        print('Error:', user_msg_serializer.errors)
        return Response(user_msg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
