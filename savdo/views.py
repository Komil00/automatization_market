from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, pagination, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)
from rest_framework.viewsets import ModelViewSet

from savdo.filters import SavdoFilter
from savdo.models import Savdo, SavdoProduct, Tolovlar, Tranzaksiya
from savdo.serializers import (SavdoCreatePostSerializers,
                               SavdoProductSerializer, SavdoProductSerializers,
                               SavdoSerializers, TolovlarGETSerializers,
                               TolovlarSerializers, TranzaksiyaSerialiers)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': "Please provide both username and password"},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Invalid Credentials"},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.object.get_or_create(user=user)
    return Response({"token": token.key},
                    status=HTTP_200_OK)


class TranzaksiyaViewSet(ModelViewSet):
    # permission_classes = [IsAdminUser]
    queryset = Tranzaksiya.objects.all()
    serializer_class = TranzaksiyaSerialiers

    def get_queryset(self):
        queryset = super().get_queryset()
        turi = self.request.query_params.get("turi")
        if turi and turi in []:
            pass
        return queryset


class SavdoPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
    queryset = Savdo.objects.all()
    filterset_class = Savdo
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'page_size': self.page_size,
            'total_objects': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


# Savdo Views
class SavdoViewSet(ModelViewSet):
    # permission_classes = [IsAdminUser]
    pagination_class = SavdoPagination
    queryset = Savdo.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user__username', 'savdo_turi', 'chegirma_turi', 'mijoz__ism_sharif', 'chegirma',
                     'vaqt']  ########New

    filterset_class = SavdoFilter
    serializer_class = SavdoSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Savdo.objects.all().order_by('-id')
        savdo_turi = self.request.query_params.get("savdo_turi")
        chegirma_turi = self.request.query_params.get("chegirma_turi")
        mijoz = self.request.query_params.get("mijoz")
        vaqt = self.request.query_params.get("vaqt")
        ombor_farq = self.request.query_params.get("ombor_farq")
        
        
        is_active = self.request.query_params.get("is_active")
        filter_data = {}
        if chegirma_turi:
            filter_data['chegirma_turi__icontains'] = chegirma_turi
        if savdo_turi:
            filter_data['savdo_turi__icontains'] = savdo_turi
        if mijoz:
            filter_data['mijoz__icontains'] = mijoz
        if is_active:
            filter_data['is_active__icontains'] = is_active
        if vaqt:
            filter_data['vaqt__icontains'] = vaqt
            
        if ombor_farq:
            filter_data['ombor_farq__icontains'] = ombor_farq
        return queryset

    @action(detail=True, methods=['get'])
    def savdo_products(self, request, pk=None):
        savdo = self.get_object()
        serializer = SavdoProductSerializers(savdo.savdo_products.all(), many=True)
        return Response(serializer.data)


class SavdoCreateView(generics.CreateAPIView):
    queryset = Savdo.objects.all()
    serializer_class = SavdoCreatePostSerializers

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        return redirect(self.get_success_url())


class SavdoListView(generics.ListAPIView):
    queryset = Savdo.objects.all().order_by('-id')
    serializer_class = SavdoSerializers


class SavdoAPIView(generics.RetrieveAPIView):
    queryset = Savdo.objects.all()
    serializer_class = SavdoSerializers
    lookup_field = "pk"


# Savdodagi sotilgan mahsulotlar views

class SavdoProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SavdoProductSerializer
    queryset = SavdoProduct.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = SavdoProductSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


########################
# Savdo Product Views


class SavdoProductViewSet(ModelViewSet):
    queryset = SavdoProduct.objects.all()
    queryset = Savdo.objects.all().order_by('-id')
    serializer_class = SavdoProductSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = SavdoProduct.objects.all().order_by('-id')
        savdo = self.request.query_params.get("savdo")
        mahsulot = self.request.query_params.get("mahsulot")
        olchov = self.request.query_params.get("olchov")
        miqdor = self.request.query_params.get("miqdor")
        narx_turi = self.request.query_params.get("narx_turi")
        sotish_turi = self.request.query_params.get("sotish_turi")
        sotish_olchov = self.request.query_params.get("sotish_olchov")
        narx = self.request.query_params.get("narx")
        total_summa = self.request.query_params.get("total_summa")
        filter_data = {}
        if mahsulot:
            filter_data['mahsulot__icontains'] = mahsulot
        if savdo:
            filter_data['savdo__icontains'] = savdo
        if olchov:
            filter_data['olchov__icontains'] = olchov
        if miqdor:
            filter_data['miqdor__icontains'] = miqdor
        if narx_turi:
            filter_data['narx_turi__icontains'] = narx_turi
        if sotish_turi:
            filter_data['sotish_turi__icontains'] = sotish_turi
        if sotish_olchov:
            filter_data['sotish_olchov__icontains'] = sotish_olchov
        if narx:
            filter_data['narx__icontains'] = narx
        if total_summa:
            filter_data['total_summa__icontains'] = total_summa
        queryset = queryset.filter(**filter_data)
        return queryset


# To'lovlar Views

class TolovViewSet(ModelViewSet):
    # permission_classes = [IsAdminUser]
    queryset = Tolovlar.objects.all()
    serializer_class = TolovlarGETSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        tranzaksiya_turi = self.request.query_params.get("tranzaksiya_turi")
        mijoz = self.request.query_params.get("mijoz")
        savdo = self.request.query_params.get("savdo")
        tolov_turi = self.request.query_params.get("tolov_turi")
        summa = self.request.query_params.get("summa")
        yaralgan_sana = self.request.query_params.get("yaralgan_sana")
        izoh = self.request.query_params.get("izoh")
        chek_id = self.request.query_params.get("chek_id")
        filter_data = {}
        if tranzaksiya_turi:
            filter_data['tranzaksiya_turi'] = tranzaksiya_turi
        if mijoz:
            filter_data['mijoz'] = mijoz
        if savdo:
            filter_data['savdo'] = savdo
        if tolov_turi:
            filter_data['tolov_turi'] = tolov_turi
        if summa:
            filter_data['summa'] = summa
        if yaralgan_sana:
            filter_data['yaralgan_sana'] = yaralgan_sana
        if izoh:
            filter_data['izoh'] = izoh
        if chek_id:
            filter_data['chek_id'] = chek_id
        queryset = queryset.filter(**filter_data)
        return queryset


class MijozTolovlarView(ListAPIView):
    # permission_classes = [IsAdminUser]
    queryset = Tolovlar.objects.all()
    serializer_class = TolovlarSerializers

    def get_queryset(self):
        result = self.queryset.filter()
        return result


# Savdo Statistika Views
class SavdoStaViewSet(ModelViewSet):
    # permission_classes = [IsAdminUser]
    queryset = Savdo.objects.all()
    serializer_class = SavdoSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Savdo.objects.all().order_by('-id')
        savdo_turi = self.request.query_params.get("savdo_turi")
        chegirma_turi = self.request.query_params.get("chegirma_turi")
        mijoz = self.request.query_params.get("mijoz")
        vaqt = self.request.query_params.get("vaqt")
        is_active = self.request.query_params.get("is_active")
        filter_data = {}
        if chegirma_turi:
            filter_data['chegirma_turi__icontains'] = chegirma_turi
        if savdo_turi:
            filter_data['savdo_turi__icontains'] = savdo_turi
        if mijoz:
            filter_data['mijoz__icontains'] = mijoz
        if is_active:
            filter_data['is_active__icontains'] = is_active
        if vaqt:
            filter_data['vaqt__icontains'] = vaqt

        queryset = queryset.filter(**filter_data)
        return queryset

    @action(detail=True, methods=['get'])
    def savdo_products(self, request, pk=None):
        savdo = self.get_object()
        serializer = SavdoProductSerializers(savdo.savdo_products.all(), many=True)
        return Response(serializer.data)
