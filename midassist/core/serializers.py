from rest_framework.serializers import ModelSerializer
from .models import TestDB


class TestDBSerializer(ModelSerializer):
    class Meta:
        model = TestDB
        fields = '__all__'
