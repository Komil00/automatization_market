from rest_framework import serializers
from django.db.models import Sum

from moliya.models import Moliya_chiqim, Omborxona, OmborCategory
from products.models import Mahsulot_olchov, Mahsulotlar
from savdo.models import Tranzaksiya
from savdo.serializers import Mahsulot_olchovSerializers, MahsulotlarSerializers, MijozSerializers, SavdoProductSerializers, TolovlarSerializers
from users.serializers import IshchiSerializers, LoginSerializer


# Tranzaksiya Serialziers
class TranzaksiyaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tranzaksiya
        fields = ('id', 'title', 'turi', 'status')


class MoliyaChiqimSerializers(serializers.ModelSerializer):
    mahsulot_nomi = MahsulotlarSerializers(read_only=True)
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
            'mahsulot_nomi',
            'olchov',
            'summa',
            'ombor_id',
            'description',
        )



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tranzaksiya_turi'] = TranzaksiyaSerializers(instance=instance.tranzaksiya_turi).data
        representation['user'] = LoginSerializer(instance=instance.user).data
        representation['ishchi'] = IshchiSerializers(instance=instance.ishchi).data
        representation['olchov'] = Mahsulot_olchovSerializers(instance=instance.olchov).data
        representation['mijoz'] = MijozSerializers(instance=instance.mijoz).data
        return representation



# Ombor Kategoriya Serializers

class OmborCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = OmborCategory
        fields = [
            'id',
            'kategoriya',
        ]

class MahsulotNomiSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mahsulotlar
        fields = ['id', 'mahsulot_nomi', 'mahsulot_format']

class OlchovSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mahsulot_olchov
        fields = ['id', 'olchov_nomi', 'olchov_format', 'olchov', 'narx', 'mahsulot_number']

# Omborxona Serializers
class OmborGetSerializers(serializers.ModelSerializer):
    mahsulot_nomi = MahsulotNomiSerializers()
    olchov = OlchovSerializers()
    class Meta:
        model = Omborxona
        fields = [
            'id',
            'user',
            'kategoriya',
            'savdo_turi',
            'mahsulot_nomi',
            'olchov',
            'miqdor',
            'narx_turi',
            'narx',
            'total_summa',
            'summa',
            'vaqt',
            'description',
            'chiqim_id',

        ]


class OmborPostSerializers(serializers.ModelSerializer):

    class Meta:
        model = Omborxona
        fields = [
            'id',
            'user',
            'kategoriya',
            'savdo_turi',
            'mahsulot_nomi',
            'olchov',
            'miqdor',
            'narx_turi',
            'narx',
            'total_summa',
            'summa',
            'vaqt',
            'description',
            'chiqim_id',

        ]