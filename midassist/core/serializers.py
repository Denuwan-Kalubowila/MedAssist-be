from rest_framework.serializers import ModelSerializer
from .models import TestDB, Member


class TestDBSerializer(ModelSerializer):
    """The class represent Database serializer"""

    class Meta:
        """The class represent Database serializer Meta data"""
        model = TestDB
        fields = '__all__'


class MemberSerializer(ModelSerializer):
    """The class represent Database serializer"""

    class Meta:
        """The class represent Database serializer Meta data"""
        model = Member
        fields = '__all__'
