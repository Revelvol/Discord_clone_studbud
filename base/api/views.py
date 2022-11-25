from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view (['GET'])
def getRoutes(request):
    routes = ['hello']
    return Response(routes)
@api_view(['GET'])
def getRooms(request):
    """rooms = Room.objects.all()  #query the database
    return Response(rooms)"""
    pass