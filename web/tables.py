from django.utils.html import format_html

import django_tables2 as tables

from . import models


class OpportunityTable(tables.Table):
    more = tables.Column(accessor='id', verbose_name='Детальніше')
    employer__scope = tables.Column(verbose_name='Сфера діяльності')
    employer__company = tables.Column(verbose_name='Компанія')

    def render_more(self, value, record):
        return format_html('<a href="{}">>>></a>', record.get_absolute_url())

    class Meta:
        model = models.Opportunity
        template_name = "django_tables2/bootstrap.html"
        fields = (
            'name', 'type', 'employer__city',
            'employer__scope', 'employer__company')
