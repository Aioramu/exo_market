from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser
from rest_framework import authentication, permissions,exceptions
from .models import Announcement,Announce_type
from .serializers import AnnounceSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly
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
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'fields':data[0].keys(),
            'results': data
        })
class AnnouncementRecordsView(generics.ListCreateAPIView):
    parser_classes = [FormParser,MultiPartParser]
    queryset = Announcement.objects.all()
    serializer_class = AnnounceSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        #serializer = AnnounceSerializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        serializer_context = {'request': request}
        serializer = self.serializer_class(
            page, context=serializer_context, many=True
        )
        return self.get_paginated_response(serializer.data)
        #return Response(serializer.data)
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
    permission_classes = (IsAuthenticatedOrReadOnly,)
    #items=collection.find_one(params['type'])
    def get(self,request):
        collection=db.get_collection("type")
        params=request.query_params
        print(params)
        match params:
            case {'type':'Animals'}:
                return Response({"fields":["animal_type","name"]})
            case {'animal_type':type}:#type->animal_type->name
                return Response({"fields":"animal_name"})
            case {'type':'Рerephriya'}:#
                return Response({"perephriya_type":["heat","decor","substrat","sensors","others"]})         #->thermal_mat or stone
            case {'perephriya_type':"heat"}:#type->perephriya_type->heat->lamp->fields
                return Response({"heat":["lamp","thermal_mat"]})#       ->decor
            case {"heat":"lamp"}:                               #       ->substrat
                return Response({"lamp":["uvb","heat"]})        #       ->sensors
            case {"lamp":"uvb"}:
                return Response({"fields":["uvb_power","power","socket"]})
            case {"lamp":"heat"}:
                return Response({"fields":["power"]})
            case _:
                items=collection.find({})
                tmp=json.loads(json_util.dumps(items))
                return Response(tmp)
                #raise exceptions.NotFound(" ")
    def post(self,request):
        collection=db.get_collection("type")
        collection.insert_one(request.data).inserted_id
        items=collection.find({})
        tmp=json.loads(json_util.dumps(items))
        return Response(tmp)


#'Animals':['']
