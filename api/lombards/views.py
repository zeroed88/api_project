from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import status, serializers
from .serializers import PercentQuerySerializer, FilialSerializer, GoldMarkSerializer
from utils.utils import get_client_ip
from django.http import Http404
from main.models import User
from .models import Filial, GoldMark

@api_view(['POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def percent(request):
    ln = request.data['surname']
    user = User.objects.get_from_auth(request.auth)
    zg = request.data['zalog']
    ip = get_client_ip(request)
    test_data = {
        'user': user.pk,
        'lastName': ln,
        'zalogNumber': zg,
        'ip': ip
    }

    s = PercentQuerySerializer(data=test_data)
    if s.is_valid():
        try:
            s.save()
            return Response(s.data)
        except:
            raise Http404
    else:
        raise Http404


@api_view(['GET'])
@permission_classes((AllowAny, ))
def filials(request):
    try:
        queryset = Filial.objects.filter(active=True)
        s = FilialSerializer(queryset, many=True)
        return Response(s.data)

    except Exception as er:
        return Response(str(er), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def goldPrices(request):
    try:
        queryset = GoldMark.objects.all()
        s = GoldMarkSerializer(queryset, many=True)
        return Response(s.data)
    except Exception as er:
        return Response(str(er), status=status.HTTP_400_BAD_REQUEST)



