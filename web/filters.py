from django.db import models

import django_filters

from .models import Opportunity


class OpportunityFilter(django_filters.FilterSet):
    class Meta:
        model = Opportunity
        fields = {
            'cost': ['gt', 'lt'],
            'name': ['icontains'],
            'employer__company': ['icontains']
        }
        filter_overrides = {
            models.BooleanField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }
