from rest_framework import serializers
from .models import User, Doctor
from .models import Message
from .models import Pdf
from .models import Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password', 'age', 'phone_number')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class PdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pdf
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['message', 'user']


class ChatSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)