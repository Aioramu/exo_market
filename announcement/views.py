from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser
from rest_framework import authentication, permissions
from .models import Announcement,Announce_type
from .serializers import AnnounceSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from pymongo import MongoClient
import json
from bson import json_util
from rest_framework.pagination import PageNumberPagination
from rest_framework.settings import api_settings
connection_string = 'mongodb://username:RooTpasS@mongodb/myFirstDatabase?retryWrites=true&w=majority'
#client = MongoClient(connection_string)

client = MongoClient('77.223.103.173:27018',
                      username='username',
                     password='RooTpasS',
                     authSource='admin')
db = client['db_name']
#collection=db.animals
#collection.insert_one(request.data).inserted_id
#items=collection.find_one({"_id": post_id})
#tmp=json.loads(json_util.dumps(items))
# Create your views here.
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
class AnnouncementRecordsView(generics.ListCreateAPIView):
    parser_classes = [FormParser,MultiPartParser]
    queryset = Announcement.objects.all()
    serializer_class = AnnounceSerializer
    pagination_class = StandardResultsSetPagination
    """
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = AnnounceSerializer(queryset, many=True)
        return Response(serializer.data)
    """
    def mongo_create(self,data,full_data):
        tmp={}

        for i in full_data.keys():
            if i not in data.keys():
                tmp[i]=full_data[i]
        collection=db.Announcement
        tmp['announce_id']=data['id']
        annunce_id=collection.insert_one(tmp).inserted_id
        items=collection.find_one({"_id": annunce_id})
        tmp=json.loads(json_util.dumps(items))
        for i in data:
            tmp[i]=data[i]
        return tmp
    def post(self,request):
        permission_classes = [permissions.IsAuthenticated]
        queryset=request.data.copy()
        queryset['user_pk']=request.user.id
        try:
            queryset['type_pk']=Announce_type.objects.get(type=queryset['type']).id
        except:
            return Response(status=404)
        print(queryset)
        serializer=AnnounceSerializer(data=queryset)
        if serializer.is_valid():
            serializer.save()
            try:
                tmp=self.mongo_create(serializer.data,request.data)
            except Exception as e:
                tmp={"error":str(e)}
                #serializer.delete()
            return Response(tmp)
        else:
            return Response(serializer.errors)
class Fields(APIView):
    types=['animals','perephriya']
    def get(self,request):
        params=request.query_params
        if 'type' in params:
            collection=db.get_collection(params['type'])
            items=collection.find_one(params['type'])
            pass
