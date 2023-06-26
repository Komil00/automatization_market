from rest_framework import serializers
from django.db.models import Sum
from moliya.models import Moliya_chiqim, Omborxona, Omborxona_Get
from products.models import Mahsulot_olchov, Mahsulotlar
from savdo.models import Tranzaksiya
from savdo.serializers import Mahsulot_olchovSerializers, MahsulotlarSerializers, MijozSerializers, SavdoProductSerializers, TolovlarSerializers
from users.serializers import IshchiSerializers, LoginSerializer


# Tranzaksiya Serialziers
class TranzaksiyaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tranzaksiya
        fields = ('id', 'title', 'turi', 'status')

class MahsulotlarForOmbor_idSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mahsulotlar
        fields = ('id', 'mahsulot_nomi')
        

class MahsulotOlchovForOmbor_idSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mahsulot_olchov
        fields = ('id', 'olchov','olchov_nomi','olchov_format')


class Ombor_idSerializers(serializers.ModelSerializer):
    mahsulot = MahsulotlarForOmbor_idSerializers(read_only=True)
    olchov = MahsulotOlchovForOmbor_idSerializers(read_only=True)
    user = LoginSerializer()
    class Meta:
        model = Omborxona
        fields = [
            'user',
            'mahsulot',
            'olchov',
            'miqdor',
        ]

class MoliyaChiqimPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Moliya_chiqim
        fields = (
            'id',
            'user',
            'nomi',
            'tranzaksiya_turi',
            'mijoz',
            'ishchi',
            'tolov_turi',
            'vaqt',
            # 'mahsulot_nomi',
            # 'olchov',
            'summa',
            'ombor_savdo',
            'tulov_status',
            'description',
        )


class MoliyaChiqimGetSerializers(serializers.ModelSerializer):
    # mahsulot_nomi = MahsulotlarSerializers(read_only=True)
    # total_miqdor = serializers.SerializerMethodField()
    ombor_savdo = Ombor_idSerializers(read_only=True)

    class Meta:
        model = Moliya_chiqim
        fields = (
            'id',
            'user',
            'nomi',
            'tranzaksiya_turi',
            'mijoz',
            'ishchi',
            'tolov_turi',
            'vaqt',
            # 'mahsulot_nomi',
            # 'olchov',
            'summa',
            'ombor_savdo',
            'tulov_status',
            'description',
        )



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tranzaksiya_turi'] = TranzaksiyaSerializers(instance=instance.tranzaksiya_turi).data
        representation['user'] = LoginSerializer(instance=instance.user).data
        representation['ishchi'] = IshchiSerializers(instance=instance.ishchi).data
        # representation['olchov'] = Mahsulot_olchovSerializers(instance=instance.olchov).data
        representation['mijoz'] = MijozSerializers(instance=instance.mijoz).data
        return representation




class MahsulotNomiSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mahsulotlar
        fields = ['id', 'mahsulot_nomi', 'mahsulot_format']

class OlchovSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mahsulot_olchov
        fields = ['id', 'olchov_nomi', 'olchov_format', 'olchov', 'narx', 'mahsulot_number']


class MoliyaChiqimOmborSerializers(serializers.ModelSerializer):
    # mahsulot_nomi = MahsulotlarSerializers(read_only=True)
    # total_miqdor = serializers.SerializerMethodField()

    class Meta:
        model = Moliya_chiqim
        fields = (
            'id',
            'user',
            'nomi',
            'tranzaksiya_turi',
            'mijoz',
            'ishchi',
            'tolov_turi',
            'vaqt',
            # 'mahsulot_nomi',
            # 'olchov',
            'summa',
            'ombor_savdo',
            'description',
        )


# Omborxona Serializers

class OmborGetSerializers(serializers.ModelSerializer): 
    mahsulot = MahsulotNomiSerializers() 
    olchov = OlchovSerializers() 
    user = LoginSerializer() 
    # moliya_chiqim = MoliyaChiqimOmborSerializers(source='ombor_moliya_chiqim',read_only=True,many=True) 
    class Meta: 
        model = Omborxona 
        fields = [ 
            'id', 
            'user', 
            'savdo_turi', 
            'mahsulot', 
            'olchov', 
            'miqdor', 
            'narx_turi', 
            'narx', 
            'total_summa', 
            'summa', 
            'vaqt', 
            # 'moliya_chiqim' 
         
        ] 
    # def to_representation(self, instance): 
    #     representation = super().to_representation(instance) 
    #     ombor = Omborxona.objects.get(id=instance.id) 
    #     summa_all = ombor.ombor_moliya_chiqim.aggregate(summa=Sum('summa')).get('summa') 
    #     representation['summa_all'] = summa_all if summa_all is not None else 0 
    #     return representation


class OmborPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Omborxona
        fields = [
            'id',
            'user',
            'savdo_turi',
            'mahsulot',
            'olchov',
            'miqdor',
            'narx_turi',
            'narx',
            'total_summa',
            'summa',
            'vaqt',
        ]

class OmborGetAllSerializers(serializers.ModelSerializer): 
    mahsulot = MahsulotNomiSerializers() 
    olchov = OlchovSerializers() 
    user = LoginSerializer() 
    moliya_chiqim = MoliyaChiqimOmborSerializers(source='ombor_moliya_chiqim',read_only=True,many=True) 
    class Meta: 
        model = Omborxona_Get 
        fields = [ 
            'id', 
            'user', 
            'savdo_turi', 
            'mahsulot', 
            'olchov', 
            'miqdor', 
            'narx_turi', 
            'narx', 
            'total_summa', 
            'summa', 
            'vaqt', 
            'moliya_chiqim' 
         
        ] 

    def to_representation(self, instance): 
        representation = super().to_representation(instance) 
        ombor = Omborxona_Get.objects.get(id=instance.id) 
        summa_all = ombor.ombor_moliya_chiqim.aggregate(summa=Sum('summa')).get('summa') 
        representation['summa_all'] = summa_all if summa_all is not None else 0 
        return representation
