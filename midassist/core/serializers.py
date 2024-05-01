from rest_framework import serializers, viewsets
from .models import User, Doctor, Pdf
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
