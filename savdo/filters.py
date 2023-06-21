from django_filters import rest_framework as filters

from .models import Savdo


class SavdoFilter(filters.FilterSet):
    vaqt = filters.DateFilter(field_name='vaqt', lookup_expr='date')

    class Meta:
        model = Savdo
        fields = ['user', 'mijoz', 'savdo_turi', 'chegirma_turi', 'vaqt']