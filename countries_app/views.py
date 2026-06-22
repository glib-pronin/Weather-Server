from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from pathlib import Path
import json

# Create your views here.

class CountriesAPIView(APIView):
    def get(self, request):
        file_path = Path(__file__).resolve().parent / 'data' / 'countries.json'
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return Response(data)