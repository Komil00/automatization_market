from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)
from rest_framework.viewsets import ModelViewSet

from moliya.models import Moliya_chiqim, Omborxona, OmborCategory
from moliya.serializers import (MoliyaChiqimPostSerializers, MoliyaChiqimGetSerializers, OmborPostSerializers,OmborGetSerializers, TranzaksiyaSerializers,
                                OmborCategorySerializers)
from products.models import Mahsulot_olchov
from savdo.models import Tranzaksiya


# Moliya chiqim Views
class MoliyaChiqimViewSet(ModelViewSet):
    queryset = Moliya_chiqim.objects.all()
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
        mahsulot_nomi = self.request.query_params.get("mahsulot_nomi")
        olchov = self.request.query_params.get("olchov")
        summa = self.request.query_params.get("summa")

        ombor_id = self.request.query_params.get("ombor_id")
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
        if mahsulot_nomi:
            filter_data['mahsulot_nomi'] = mahsulot_nomi
        if olchov:
            filter_data['olchov'] = olchov
        if summa:
            filter_data['summa'] = summa

        if ombor_id:
            filter_data['ombor_id'] = ombor_id
        if description:
            filter_data['description'] = description

        queryset = queryset.filter(**filter_data)
        return queryset



# Tranzaksiya Views
class TranzaksiyaViewSet(ModelViewSet):
    queryset = Tranzaksiya.objects.all()
    serializer_class = TranzaksiyaSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        turi = self.request.query_params.get("turi")
        if turi and turi in []:
            pass
        return queryset

# Ombor Category ViewSet

class OmborCategoryViewSet(ModelViewSet):
    queryset = OmborCategory.objects.all()
    serializer_class = OmborCategorySerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        kategoriya = self.request.query_params.get("kategoriya uchun")
        filter_data = {}
        if kategoriya:
            filter_data['kategoriya__icontains'] = kategoriya
        queryset = queryset.filter(**filter_data)
        return queryset


# Omborxona Views
class OmborViewSet(ModelViewSet):
    queryset = Omborxona.objects.all()
    serializer_class = OmborGetSerializers

    def get_serializer_class(self):        
        if self.action in ['list']:
            return OmborGetSerializers
        return OmborPostSerializers
    

    def get_queryset(self):
        queryset = super().get_queryset()
        savdo_turi = self.request.query_params.get("savdo_turi")
        kategoriya = self.request.query_params.get("kategoriya_ombor")
        mahsulot_nomi = self.request.query_params.get("mahsulot_nomi")
        olchov = self.request.query_params.get("olchov")
        total_summa = self.request.query_params.get("total_summa")
        miqdor = self.request.query_params.get("miqdor")
        narx = self.request.query_params.get("narx")
        narx_turi = self.request.query_params.get("narx_turi")
        summa = self.request.query_params.get("summa")
        vaqt = self.request.query_params.get("ombor_vaqt")
        chiqim_id = self.request.query_params.get("chiqim_id")

        filter_data = {}
        if savdo_turi:
            filter_data['savdo_turi__icontains'] = savdo_turi
        if kategoriya:
            filter_data['kategoriya__icontains'] = kategoriya
        if mahsulot_nomi:
            filter_data['mahsulot_nomi__icontains'] = mahsulot_nomi
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
        if chiqim_id:
            filter_data['chiqim_id__icontains'] = chiqim_id

        queryset = queryset.filter(**filter_data)
        return queryset


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
