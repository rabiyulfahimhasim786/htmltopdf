#from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from rest_framework.response import Response
from .serializers import PdfSerializer#, StandardsSerializer, CountriesSerializer, TagSerializer

from .models import Pdf#, Standards, Countries, Tag

from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
# Create your views here.
from django.http import HttpResponse
# Create your views here.
from django.http import HttpResponse

import img2pdf
from PIL import Image
import os
import pdfkit
import imgkit
def index(request):
    return HttpResponse("Hello, world!")


class PdfList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        currencies = Pdf.objects.all()
        serializer = PdfSerializer(currencies, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PdfSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PdfDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Pdf.objects.get(pk=pk)
        except Pdf.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        currencies = self.get_object(pk)
        serializer = PdfSerializer(currencies)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        currencies = self.get_object(pk)
        serializer = PdfSerializer(currencies, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



def pdfurl(request):
    documents = Pdf.objects.all()
    #rank = Document.objects.latest('id')
    #print(rank)
    for obj in documents:
        rank = obj.link
        num  =  obj.name
        #print(rank)
    #print(rank[8:-5])
    #print('/media/'+rank[8:-5]+'.pdf')
    #pdfkit.from_url(rank, './media/pdf/'+str(num)+'.pdf')
    pdfkit.from_url(rank, './media/pdf/'+num+'.pdf')
    return HttpResponse("Hello, world!")



def imgurl(request):
    documents = Pdf.objects.all()
    #rank = Document.objects.latest('id')
    #print(rank)
    for obj in documents:
        img = obj.link
        numb = obj.number
        #print(img)
    #print(img[8:-5])
    #print('/media/'+img[8:-5]+'.jpg')
    imgkit.from_url(img, './media/img/'+str(numb)+'.jpg')
    #return HttpResponse("Hello, world!")
    return redirect('imgtopdf')


def imgtopdf(request):
    documents = Pdf.objects.all()
    #rank = Document.objects.latest('id')
    #print(rank)
    for obj in documents:
        img = obj.link
        numb = obj.number
        #print(img)
    #print(img[8:-5])
    #print('/media/'+img[8:-5]+'.jpg')
    #imgkit.from_url(img, './media/img/'+str(numb)+'.jpg')
    img_path =  './media/img/'+str(numb)+'.jpg'

    # storing pdf path
    pdf_path = './media/img/'+str(numb)+'.pdf'

    # opening image
    image = Image.open(img_path)

    # converting into chunks using img2pdf
    pdf_bytes = img2pdf.convert(image.filename)

    # opening or creating pdf file 
    file = open(pdf_path, "wb")

    # writing pdf files with chunks
    file.write(pdf_bytes)

    # closing image file
    image.close()

    # closing pdf file
    file.close()
    return HttpResponse("Hello, world!")
