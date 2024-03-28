from rest_framework.serializers import ModelSerializer
from .models import TestDB


class TestDBSerializer(ModelSerializer):
    """The class represent Database serializer"""
    class Meta:
        """The class represent Database serializer Meta data"""
        model = TestDB
        fields = '__all__'
