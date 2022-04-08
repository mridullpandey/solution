from django.shortcuts import render,redirect
from django.http import JsonResponse
from rest_framework import serializers

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.renderers import JSONRenderer

from urllib.parse import urlencode
import requests,environ
# Create your views here.
env = environ.Env()
environ.Env.read_env()
geolocation_data={}
def get_lat_lng(address):
    endpoint='https://maps.googleapis.com/maps/api/geocode/json'
    key=env('KEY')
    params={"address":address,'key':key}
    url_params=urlencode(params)
    url=f"{endpoint}?{url_params}"
    r=requests.get(url)
    if r.json()['status']!='OK':
        return 91,91
    lat_lng=r.json()['results'][0]['geometry']['location']
    return lat_lng['lat'],lat_lng['lng']

def address_to_geolocation(data):
    global geolocation_data

    lat,lng=get_lat_lng(data['address'])
    if lat==91:
        geolocation_data["coordinates"]={"lat":0.0,'lng':0.0}
        geolocation_data['address']="Enter valid address"
    else:
        geolocation_data["coordinates"]={"lat":lat,'lng':lng}
        geolocation_data['address']=data['address']        
    return geolocation_data

def index(request):
    return render(request,'index.html')



class Location(APIView):
    
    renderer_classes = [JSONRenderer]
    def get(self,request,*args,**kwargs):
        data={
            'message': 'please use post request on postman',
        }
        return Response(data)

    def post(self,request,*args,**kwargs):
        self.renderer_classes = [JSONRenderer, ]
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            geolocation_data=address_to_geolocation(request.data)
            output_format=request.data['output_format']
            if output_format.lower()=='json':
                return Response(geolocation_data)
            else:
                
                return(redirect('/xml'))
        else:
            return Response(serializer.errors)

class XmlView(APIView):
    renderer_classes = [XMLRenderer]
    def get(self, request,*args,**kwargs):
        global geolocation_data
        return Response(geolocation_data)
