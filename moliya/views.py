from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from moliya.models import Moliya_chiqim, Omborxona, Omborxona_Get
from moliya.serializers import (MoliyaChiqimPostSerializers, MoliyaChiqimGetSerializers, OmborGetAllSerializers, OmborPostSerializers,OmborGetSerializers, OmborPutPutchAllSerializers, TranzaksiyaSerializers)
from products.models import Mahsulot_olchov, Mahsulotlar
from savdo.models import Tranzaksiya
from users.models import User



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
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



# Moliya chiqim Views
class MoliyaChiqimViewSet(ModelViewSet):
    queryset = Moliya_chiqim.objects.all().order_by('-id')
    serializer_class = MoliyaChiqimGetSerializers

    
    def get_serializer_class(self):        
        if self.action in ['list']:
            return MoliyaChiqimGetSerializers
        return MoliyaChiqimPostSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        tranzaksiya_turi = self.request.query_params.get('tranzaksiya_turi')
        mijoz = self.request.query_params.get("mijoz")
        ishchi = self.request.query_params.get("ishchi")
        tolov_turi = self.request.query_params.get("tolov_turi")
        tulov_status = self.request.query_params.get("tulov_status")
        # olchov = self.request.query_params.get("olchov")
        summa = self.request.query_params.get("summa")

        ombor_savdo = self.request.query_params.get("ombor_savdo")
        description = self.request.query_params.get("description")

        filter_data = {}
        if tranzaksiya_turi:
            filter_data['tranzaksiya_turi'] = tranzaksiya_turi
        if mijoz:
            filter_data['mijoz'] = mijoz
        if ishchi:
            filter_data['ishchi'] = ishchi
        if tolov_turi:
            filter_data['tolov_turi'] = tolov_turi
        # if mahsulot_nomi:
        #     filter_data['mahsulot_nomi'] = mahsulot_nomi
        if tulov_status:
            filter_data['tulov_status'] = tulov_status
        if summa:
            filter_data['summa'] = summa

        if ombor_savdo:
            filter_data['ombor_savdo'] = ombor_savdo
        if description:
            filter_data['description'] = description

        queryset = queryset.filter(**filter_data)
        return queryset



# Tranzaksiya Views
class TranzaksiyaViewSet(ModelViewSet):
    queryset = Tranzaksiya.objects.all().order_by('-id')
    serializer_class = TranzaksiyaSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        turi = self.request.query_params.get("turi")
        if turi and turi in []:
            pass
        return queryset


# Omborxona Views
class OmborViewSet(ModelViewSet):
    queryset = Omborxona.objects.all().order_by('-id')
    serializer_class = OmborGetSerializers
    http_method_names = ['post']

    def get_serializer_class(self):        
        if self.action in ['list']:
            return OmborGetSerializers
        return OmborPostSerializers
    def get_queryset(self):
        queryset = super().get_queryset()
        savdo_turi = self.request.query_params.get("savdo_turi")
        mahsulot = self.request.query_params.get("mahsulot")
        olchov = self.request.query_params.get("olchov")
        total_summa = self.request.query_params.get("total_summa")
        miqdor = self.request.query_params.get("miqdor")
        narx = self.request.query_params.get("narx")
        narx_turi = self.request.query_params.get("narx_turi")
        summa = self.request.query_params.get("summa")
        vaqt = self.request.query_params.get("ombor_vaqt")

        filter_data = {}
        if savdo_turi:
            filter_data['savdo_turi__icontains'] = savdo_turi
        if mahsulot:
            filter_data['mahsulot__icontains'] = mahsulot
        if olchov:
            filter_data['olchov__icontains'] = olchov
        if total_summa:
            filter_data['total_summa__icontains'] = total_summa
        if miqdor:
            filter_data['miqdor__icontains'] = miqdor
        if narx:
            filter_data['narx__icontains'] = narx
        if narx_turi:
            filter_data['narx_turi__icontains'] = narx_turi
        if summa:
            filter_data['summa__icontains'] = summa
        if vaqt:
            filter_data['vaqt__icontains'] = vaqt
        queryset = queryset.filter(**filter_data)
        return queryset

    def create(self, request, *args, **kwargs):
        omborxona_serializer = OmborPostSerializers(data=self.request.data)
        omborxona_serializer.is_valid(raise_exception=True)
        omborxona_serializer.save()
        self.perform_create(omborxona_serializer)
        return Response(status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        user_id = self.request.data.get('user')
        user = User.objects.get(id=user_id)
        savdo_turi = self.request.data.get('savdo_turi')
        mahsulot_id = self.request.data.get('mahsulot')
        mahsulot = Mahsulotlar.objects.get(id=mahsulot_id)
        olchov_id = self.request.data.get('olchov')
        olchov = Mahsulot_olchov.objects.get(id=olchov_id)
        total_summa = self.request.data.get('total_summa')
        miqdor = self.request.data.get('miqdor')
        narx = self.request.data.get('narx')
        narx_turi = self.request.data.get('narx_turi')
        vaqt = self.request.data.get('vaqt')

        create_ombor = Omborxona_Get.objects.create(
            user=user,
            savdo_turi=savdo_turi,
            mahsulot=mahsulot,
            olchov=olchov,
            miqdor=miqdor,
            narx=narx,
            narx_turi=narx_turi,
            vaqt=vaqt,
            total_summa=total_summa
        )
        create_ombor.save()


class OmborGetViewSet(ModelViewSet):
    queryset = Omborxona_Get.objects.all().order_by('-id')
    serializer_class = OmborGetAllSerializers
    http_method_names = ['get','put','putch','delete']

    def get_serializer_class(self):        
        if self.action in ['list']:
            return OmborGetAllSerializers
        return OmborPutPutchAllSerializers