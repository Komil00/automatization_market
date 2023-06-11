from rest_framework import serializers

from moliya.models import Moliya_chiqim, Tranzaksiya, Omborxona
from products.models import Mahsulot_olchov, Mahsulotlar
from savdo.models import Savdo, SavdoProduct, Tolovlar
from users.models import Mijoz
from users.serializers import LoginSerializer


# Tranzaksiya Serializers - Moliya bo'limidagi Qanday turdagi kirim va chiqim uchun
class TranzaksiyaSerialiers(serializers.ModelSerializer):
    class Meta:
        model = Tranzaksiya
        fields = ('id', 'title', 'turi', 'status')


# Tolovlar Serializers - Moliya kirim uchun - Mijoz Savdo qilganda to'lov qilish uchun
class TolovlarSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tolovlar
        fields = (
            'id',
            'user',
            'savdo',
            'tranzaksiya_turi',
            'tolov_turi',
            'muddat',
            'summa',
            'status',
            'yaralgan_sana',
            'izoh',
            'chek_id'
        )

    def get_chek_id(self, instance):
        tolovlar_instances = Tolovlar.objects.filter(savdo=instance)
        if tolovlar_instances.exists():
            return tolovlar_instances[0].chek_id
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['savdo'] = SavdoForMijozSerializer(instance=instance.savdo).data
        representation['user'] = LoginSerializer(instance=instance.user).data
        representation['tranzaksiya_turi'] = TranzaksiyaSerialiers(instance=instance.tranzaksiya_turi).data
        return representation
    
class ForSavdolarMiqdorSerializers(serializers.ModelSerializer):
    class Meta:
        model = SavdoProduct
        fields = ['miqdor']

class OlchovlarSerializers(serializers.ModelSerializer):
    class Meta:
        model = Omborxona
        fields = ['miqdor']

# Mahsulot o'lchov Serializers - Mahsulot nom, formati orqali unga narx berish
class Mahsulot_olchovSerializers(serializers.ModelSerializer):
    umumiy_ombordagi_miqdori = OlchovlarSerializers(source='ombor_olchovi', many=True, read_only=True)

    class Meta:
        model = Mahsulot_olchov
        fields = ('id', 'mahsulot_number', 'olchov', 'narx', 'olchov_nomi', 'olchov_format', 'umumiy_ombordagi_miqdori')

    def get_sum_dict(self, dict1, dict2):

        sum_dict = dict1.copy()

        for key, value in dict2.items():
            if key in sum_dict:
                sum_dict[key] -= value
            else:
                sum_dict[key] = value

        return sum_dict
    def get_sum_of_dicts(self, dictionaries):
        result_dict = {}

        for dictionary in dictionaries:
            for key, value in dictionary.items():
                result_dict[key] = result_dict.get(key, 0) + value

        return result_dict
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        savdolar_miqdor_instances = SavdoProduct.objects.filter(id=instance.id)
        savdolar_miqdori = ForSavdolarMiqdorSerializers(savdolar_miqdor_instances, many=True).data
        representation['sum_of_umumiy_ombordagi_miqdori'] = self.get_sum_of_dicts(representation['umumiy_ombordagi_miqdori'])
        representation['sum_of_savdolar_miqdori'] = self.get_sum_of_dicts(savdolar_miqdori)
        representation['joriy_ombordagi_miqdor'] = self.get_sum_dict(representation['sum_of_umumiy_ombordagi_miqdori'],
                                                       representation['sum_of_savdolar_miqdori'])
        representation['sum_of_umumiy_ombordagi_miqdori'] = sum(representation['sum_of_umumiy_ombordagi_miqdori'].values())
        representation['sum_of_savdolar_miqdori'] = sum(representation['sum_of_savdolar_miqdori'].values())
        representation['joriy_ombordagi_miqdor'] = sum(representation['joriy_ombordagi_miqdor'].values())

        return representation

# Mahsulotlar Serializers - Mahsulot o'lchov orqali uning barcha ma'lumotlari

class MahsulotlarSerializers(serializers.ModelSerializer):
    mahsulot_olchov = Mahsulot_olchovSerializers(many=True, read_only=True)

    class Meta:
        model = Mahsulotlar
        fields = ('id', 'mahsulot_nomi', 'mahsulot_format', 'mahsulot_olchov')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        mahsulot_olchov_instances = Mahsulot_olchov.objects.filter(mahsulot_number=instance)
        if mahsulot_olchov_instances.exists():
            representation['mahsulot_olchov'] = Mahsulot_olchovSerializers(mahsulot_olchov_instances, many=True).data
        return representation



# Savdo Mahsulot Serializers -  GET uchun Savdo qilingan Mahsulotlar ro'yxati
class SavdoMahsulotlarSerializers(serializers.ModelSerializer):
    mahsulot_olchov = Mahsulot_olchovSerializers(many=True, read_only=True)

    class Meta:
        model = Mahsulotlar
        fields = ('id', 'mahsulot_nomi', 'mahsulot_format', 'mahsulot_olchov')


# Savdo For Mijoz Serialziers - Mijozning qilgan savdolari GET metodda ko'rinishi
class MahsulotlarForSavdoProMijozSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mahsulotlar
        fields = ['mahsulot_nomi']


class OlchovForSavdoProMijozSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mahsulot_olchov
        fields = ['id']


# Mijoz sotib olgan mahsulot turlari, nom va formatlari
class SavdoProMijozSerializers(serializers.ModelSerializer):
    class Meta:
        model = SavdoProduct
        fields = '__all__'
        depth = 2


class SavdoForMijozSerializer(serializers.ModelSerializer):
    user = LoginSerializer(read_only=True)
    tolovlar = TolovlarSerializers(read_only=True, many=True)
    products = SavdoProMijozSerializers(source='savdo_products', read_only=True, many=True)

    class Meta:
        model = Savdo
        fields = (
            'id',
            'user',
            'savdo_turi',
            'chegirma_turi',
            'vaqt',
            'total_summa',
            'tolovlar',
            # 'tolovlar_mijozlar',
            'get_mijoz_total_sum',
            'get_mahsulot_total_sum',
            'chegirma',
            'products',
            # 'ombor_farq'

        )
        depth = 3


# Mijoz Serializers - Mijozning ma'lumotlar va u qilgan Savdolari haqidagi ma'lumotlar
class MijozSerializers(serializers.ModelSerializer):
    savdolar = SavdoForMijozSerializer(read_only=True, many=True)

    class Meta:
        model = Mijoz
        fields = [
            'id',
            'customer_type',
            'ism_sharif',
            'telefon',
            'izoh',
            'savdolar',
        ]


# Mijoz For Savdo Serializers - Savdo GET da Mijoz haqidagi to'liq ma'lumotlar
class MijozForSavdo(serializers.ModelSerializer):
    class Meta:
        model = Mijoz
        fields = [
            'id',
            'customer_type',
            'ism_sharif',
            'telefon',
            'izoh',
        ]

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            representation['olchov'] = Mahsulot_olchovSerializers(instance=instance.olchov).data
            return representation


# Tolovlar GET Serialzers - Mijozning Qaysi savdo uchun qancha summa to'lagani haqidagi to'liq ma'lumotlar
class TolovlarGETSerializers(serializers.ModelSerializer):
    mijoz = MijozForSavdo(read_only=True, many=True)
    savdolar = SavdoForMijozSerializer(read_only=True, many=True)

    class Meta:
        model = Tolovlar
        fields = (
            'user',
            'id',
            'mijoz',
            'savdo',
            'tranzaksiya_turi',
            'tolov_turi',
            'savdolar',
            'muddat',
            'yaralgan_sana',
            'summa',
            'izoh',
            'chek_id',

        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['savdo'] = SavdoForMijozSerializer(instance=instance.savdo).data
        representation['user'] = LoginSerializer(instance=instance.user).data
        representation['tranzaksiya_turi'] = TranzaksiyaSerialiers(instance=instance.tranzaksiya_turi).data
        return representation


# Savdo Serializers - Mijozning qilgan savdolari ma'lumotlari
class SavdoSerializers(serializers.ModelSerializer):
    user = LoginSerializer(read_only=True)
    mijoz = MijozForSavdo(read_only=True)
    tolovlar_mijozlar = TolovlarSerializers(read_only=True, many=True)
    chek_id = serializers.SerializerMethodField()

    class Meta:
        model = Savdo
        fields = (
            'id',
            'user',
            'savdo_turi',
            'chegirma_turi',
            'mijoz',
            'vaqt',
            'get_mijoz_total_sum',
            'tolovlar_mijozlar',
            'get_mahsulot_total_sum',
            'chegirma',
            'total_summa',
            'chek_id',
        )

    def get_chek_id(self, instance):
        tolovlar_instances = Tolovlar.objects.filter(savdo=instance)
        if tolovlar_instances.exists():
            return tolovlar_instances[0].chek_id
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['count'] = Savdo.objects.count()
        representation['products'] = SavdoProductSerializers(instance=instance.savdo_products, many=True).data
        return representation


# Savdo Create POST Serializers - Savdolarda POST metodi uchun
class SavdoCreatePostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Savdo
        fields = (
            'id',
            'user',
            'savdo_turi',
            'chegirma_turi',
            'mijoz',
            'vaqt',
            'get_mijoz_total_sum',
            'chegirma',
        )
        extra_kwargs = {
            'get_mijoz_total_sum': {'read_only': True},
        }


# Savdo Product Serializers - Bir vaqtning o'zida Ko'p Mahsulotlar sotib Savdo qilish uchun
class SavdoProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = SavdoProduct
        mahsulot = serializers.SerializerMethodField()
        fields = (
            'id',
            'savdo',
            'mahsulot',
            'olchov',
            'miqdor',
            'narx_turi',
            'narx',
            'sotish_turi',
            'sotish_olchov',
            'total_summa',
            'umumiy'
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['count'] = SavdoProduct.objects.count()
        representation['mahsulot'] = SavdoMahsulotlarSerializers(instance=instance.mahsulot).data
        representation['olchov'] = Mahsulot_olchovSerializers(instance=instance.olchov).data
        return representation


# Savdo Product Create Serializers - Bir vaqtning o'zida Ko'p Mahsulotlar sotib Savdo qilish uchun GET metodida
class BulkSavdoProductSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        savdo_products = [SavdoProduct(**item) for item in validated_data]
        return SavdoProduct.objects.bulk_create(savdo_products)


class SavdoProductSerializer(serializers.ModelSerializer):
    olchov = serializers.PrimaryKeyRelatedField(queryset=Mahsulot_olchov.objects.all())

    class Meta:
        model = SavdoProduct
        fields = '__all__'
        list_serializer_class = BulkSavdoProductSerializer


class SavdoProductCreatePostSerializers(serializers.ModelSerializer):
    class Meta:
        model = SavdoProduct
        fields = (
            'id', 'mahsulot', 'olchov', 'miqdor', 'narx', 'ombor_miqdor_id')

    def create(self, validated_data):
        summa = validated_data.pop('narx')
        miqdor = validated_data.pop('miqdor')
        
        # Ombordagi mahsulotga qarab Savdo miqdorni taqqoslash funksiyasi
        ombor_miqdor_id = validated_data.pop('ombor_miqdor_id')
        ombor_miqdor = Moliya_chiqim.objects.filter(id=ombor_miqdor_id)

        if miqdor < ombor_miqdor.miqdor:
            mahsulot = validated_data.pop('mahsulot')
            savdo_many = SavdoProduct.objects.create(**validated_data)
            savdo_many.mahsulot = mahsulot
            savdo_many.miqdor = miqdor
            savdo_many.narx = summa
            savdo_many.save()
            return savdo_many
        
        else:
            return 'Siz kiritgan miqdor juda kop'