from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, viewsets, permissions
from .serializers import ConfigSerializer
from .models import Config


class ConfigViewset(viewsets.ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    def get_queryset(self):
        Name = self.request.query_params.get('name')
        if Name is None :
            return Config.objects.all()
        queryset = Config.objects.filter(name=Name)
        return queryset

# @api_view(['GET','POST'])
# def configList(request):
#     if request.method == 'GET':
#         Configs = Config.objects.all().order_by('-name')
#         serializer = ConfigSerializer(Configs, many=True)
#         return Response(serializer.data)
#     if request.method == 'POST':    
#         serializer = ConfigSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)

# @api_view(['GET','POST','DELETE'])
# def configDetail(request, pk):
#     if request.method == 'GET':
#         Configs = Config.objects.get(name=pk)
#         serializer = ConfigSerializer(Configs, many=False)
#         return Response(serializer.data)
#     if request.method == 'POST':
#         config = Config.objects.get(name=pk)
#         serializer = ConfigSerializer(instance=config, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)
#     if request.method == 'DELETE':
#         config = Config.objects.get(name=pk)
#         config.delete()
#         return Response('Item succsesfully delete!')           

 