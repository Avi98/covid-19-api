from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
# Create your views here.


def merge_list(contryList, latlng):
    mergedData = []
    for data in contryList:
        for lat in latlng:
            if(data['country'] == lat['name']):
                merge = {**data, **lat}
                mergedData.append(merge)
    return mergedData


def getCoronaData():
    response = list(requests.get('https://corona.lmao.ninja/countries').json())
    latlng = list(requests.get(
        'https://restcountries.eu/rest/v2/all?fields=name;latlng;alpha2Code;alpha3Code').json())

    response.sort(key=lambda x: x['country'])
    latlng.sort(key=lambda x: x['name'])

    mergedList = merge_list(response, latlng)
    return mergedList


class Root(APIView):
    name = 'root'
    response = {
        'data': getCoronaData()
    }

    def get(self, request):
        # value = request.GET('https://corona.lmao.ninja/countries')
        return Response(self.response)
