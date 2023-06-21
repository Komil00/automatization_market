from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)
from rest_framework.viewsets import ModelViewSet

from products.models import Analitika, Mahsulot_olchov, Mahsulotlar
from products.serializers import AnalitikaSerializers
from savdo.serializers import (Mahsulot_olchovSerializers,
                               MahsulotlarSerializers, MijozSerializers)
from users.models import Ishchi, Mijoz
from users.serializers import IshchiSerializers


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")  # noqa
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


class MahsulotlarViewSet(ModelViewSet):
    queryset = Mahsulotlar.objects.all()
    serializer_class = MahsulotlarSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Mahsulotlar.objects.all().order_by('-id')
        mahsulot_nomi = self.request.query_params.get("mahsulot_nomi")
        mahsulot_format = self.request.query_params.get("mahsulot_format")
        filter_data = {}
        if mahsulot_nomi:
            filter_data['mahsulot_nomi__icontains'] = mahsulot_nomi
        if mahsulot_format:
            filter_data['mahsulot_format'] = mahsulot_format
        queryset = queryset.filter(**filter_data)
        return queryset

    @action(detail=True)
    def mahsulot_olchovs(self, request, pk=None):
        mahsulotlar = self.get_object()
        mahsulot_olchovs = Mahsulot_olchov.objects.filter(mahsulot_number=mahsulotlar)
        serializer = Mahsulot_olchovSerializers(mahsulot_olchovs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MahsulotOlchovViewSet(ModelViewSet):
    queryset = Mahsulot_olchov.objects.all()
    serializer_class = Mahsulot_olchovSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        olchov = self.request.query_params.get("olchov")
        olchov_nomi = self.request.query_params.get("olchov_nomi")
        olchov_format = self.request.query_params.get("olchov_format")
        filter_data = {}
        if olchov:
            filter_data['olchov_id'] = olchov
        if olchov:
            filter_data['olchov'] = olchov
        if olchov_format:
            filter_data['olchov_format'] = olchov_format
        if olchov_nomi:
            filter_data['olchov_nomi'] = olchov_nomi
        queryset = queryset.filter(**filter_data)
        return queryset


class MijozViewSet(ModelViewSet):
    queryset = Mijoz.objects.all()
    serializer_class = MijozSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        ism_sharif = self.request.query_params.get("ism_sharif")
        telefon = self.request.query_params.get("telefon")
        vaqt = self.request.query_params.get("vaqt")
        filter_data = {}
        if ism_sharif:
            filter_data['ism_sharif__icontains'] = ism_sharif
        if telefon:
            filter_data['telefon__icontains'] = telefon
        if vaqt:
            filter_data['vaqt__icontains'] = vaqt
        queryset = queryset.filter(**filter_data)
        return queryset


class IshchiViewSet(ModelViewSet):
    queryset = Ishchi.objects.all()
    serializer_class = IshchiSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        lavozim = self.request.query_params.get("lavozim")
        ism_sharif = self.request.query_params.get("ism_sharif")
        telefon = self.request.query_params.get("telefon")
        filter_data = {}
        if ism_sharif:
            filter_data['ism_sharif__icontains'] = ism_sharif
        if lavozim:
            filter_data['lavozim__icontains'] = lavozim

        if telefon:
            filter_data['telefon__icontains'] = telefon
        queryset = queryset.filter(**filter_data)
        return queryset


class AnalitikaViewSet(ModelViewSet):
    queryset = Analitika.objects.all()
    serializer_class = AnalitikaSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        count = self.request.query_params.get("count")
        filter_data = {}
        if count:
            filter_data['count'] = count
        queryset = queryset.filter(**filter_data)
        return queryset


class MijozOrderHistoryView(RetrieveAPIView):
    queryset = Mijoz.objects.all()
    serializer_class = MijozSerializers

    def get_object(self):
        print("pk", self.kwargs.get("pk"))
        mijoz = Mijoz.objects.filter(id=self.kwargs.get("pk")).first()
        print("mijoz", mijoz)
        return mijoz