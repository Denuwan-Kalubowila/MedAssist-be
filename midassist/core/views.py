from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TestDBSerializer
from .models import TestDB


@api_view(['GET'])
def your_view(request):
    routes = [
        {
            'test': 'test',
            'method': 'method',
        }
    ]
    return Response(routes)


@api_view(['GET'])
def testdb(request):
    test_db = TestDB.objects.all()
    serializer = TestDBSerializer(test_db, many=True)
    return Response(serializer.data)


# to get one value
@api_view(['GET'])
def testdb_one(request, pk):
    testdb_one = TestDB.objects.get(id=pk)
    serializer = TestDBSerializer(testdb_one, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def create_value(request):
    data = request.data

    test_db = TestDB.objects.create(
        body=data['body']
    )
    serializer = TestDBSerializer(test_db, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def update_value(request, pk):
    data = request.data

    testdb = TestDB.objects.get(id=pk)
    serializer = TestDBSerializer(testdb, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def delete_value(request, pk):
    test_db = TestDB.objects.get(id=pk)
    test_db.delete()
    return Response('Delete')