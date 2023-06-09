from rest_framework import serializers

from moliya.models import Moliya_chiqim, Omborxona
from products.models import Analitika, Mahsulotlar
from users.models import Ishchi, Mijoz


class AnalitikaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Analitika
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['count'] = Analitika.objects.count()
        representation['count'] = Mahsulotlar.objects.count()
        representation['count'] = Mijoz.objects.count()
        representation['count'] = Ishchi.objects.count()
        representation['count'] = Omborxona.objects.count()
        representation['count'] = Moliya_chiqim.objects.count()

        return representation