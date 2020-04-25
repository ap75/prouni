from django.db import models

import django_filters

from .models import Opportunity


class OpportunityFilter(django_filters.FilterSet):
    type = django_filters.ChoiceFilter(choices=Opportunity.TYPE_CHOICES)
    name = django_filters.CharFilter(lookup_expr='icontains')
    employer__city = django_filters.AllValuesFilter(label='Місто')
    employer__scope = django_filters.AllValuesFilter(label='Сфера діяльності')
    employer__company = django_filters.AllValuesFilter(
        label='Компанія або навчальний заклад')

    class Meta:
        model = Opportunity
        fields = ()
