import django_tables2 as dts

from . import models


class OpportunityTable(dts.Table):

    class Meta:
        model = models.Opportunity
        template_name = "django_tables2/bootstrap.html"
        fields = ('name', 'type', 'employer__company', 'descr')
