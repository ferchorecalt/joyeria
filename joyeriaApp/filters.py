import django_filters
from .models import Marca

class MarcaFilter(django_filters.FilterSet):
    class Meta:
        model = Marca
        fields = ['nombre']