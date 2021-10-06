from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser
from rest_framework import authentication, permissions
from .models import User,Location,Metro,City
from .serializers import UserSerializer,AuthSerializer,LocationSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
# Create your views here.


class MySettings(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    parser_classes = [FormParser,MultiPartParser]

    serializer_class = UserSerializer
    def get(self, request, format=None):
        permission_classes = [permissions.IsAuthenticated]
        """
        Return a users settings.
        """
        queryset = request.user
        serializer = UserSerializer(queryset)
        print(serializer)
        return Response(serializer.data)
    def post(self, request, format=None):
        permission_classes = [permissions.AllowAny]
        serializer=AuthSerializer(request.data)
        user=authenticate(**serializer.data)
        return Response({'token':user.token})
    def put(self, request, format=None):
        #authentication_classes = [authentication.TokenAuthentication]
        queryset = request.user
        data=request.data.copy()
        fields=dict(LocationSerializer().fields).keys()
        j={}
        for i in data:
            if i in fields:
                j[i]=data[i]
                if queryset.location !=None:
                    location_serializer=LocationSerializer(queryset.location,data=request.data, partial=True)
                    if location_serializer.is_valid():
                        location_serializer.save()
                    else:
                        return Response(location_serializer.errors)
                else:
                    location_serializer=LocationSerializer(data=request.data)
                    if location_serializer.is_valid():
                        location_serializer.save()
                    else:
                        return Response(location_serializer.errors)
                break
        if len(j.keys())>=1:
            data['location_pk']=location_serializer.data['id']
        print(data)
        serializer = UserSerializer(queryset,data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
        #
        return Response(serializer.data)

class Registration(APIView):
    permission_classes = [permissions.AllowAny]
    #authentication_classes = [authentication.TokenAuthentication]
    serializer_class=UserSerializer()
    parser_classes = [FormParser,MultiPartParser]
    def post(self,request):
        fields=dict(LocationSerializer().fields).keys()
        data=request.data.copy()
        j={}
        for i in data:
            if i in fields:
                j[i]=data[i]
                location_serializer=LocationSerializer(data=request.data)
                if location_serializer.is_valid():
                    location_serializer.save()
                else:
                    return Response(location_serializer.errors)
                break

        data['location_pk']=location_serializer.data['id']
        data['role']="user"
        serializer=UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            l=Location.objects.get(id=location_serializer.data['id'])
            l.delete()
            return Response(serializer.errors)
        return Response(serializer.data)
class Metros(APIView):

    def post(self, request):
        city=City.objects.get(city="Москва")
        for i in request.data:
            for j in i['stations']:
                try:
                    Metro.objects.create(station=j,city=city)
                except:
                    continue
        return Response()
    def get(self, request):
        stations=Metro.objects.all()
        st=[]
        for i in stations:
             st.append(i.station)
        return Response(st)
class Citys(APIView):
    def post(self, request):
        for i in request.data:
            try:
                City.objects.create(city=i['city'])
            except:
                continue
        return Response()
    def get(self, request):
        cities=City.objects.all()
        ci=[]
        for i in cities:
             ci.append(i.city)
        return Response(ci)
