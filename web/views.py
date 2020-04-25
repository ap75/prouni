from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from . import models, admin, tables, filters


class IndexView(TemplateView):
    template_name = 'web/index.html'
    extra_context = {
        'site_header': admin.admin_site.site_header,
        'site_title': admin.admin_site.site_title,
        'title': 'Це головна сторінка',
        'promo': models.Opportunity.objects.order_by('-id')[:3]
    }


class OpportunityList(SingleTableMixin, LoginRequiredMixin, FilterView):
    template_name = 'web/list.html'
    table_class = tables.OpportunityTable
    filterset_class = filters.OpportunityFilter
    paginate_by = 20
    extra_context = {
        'site_header': admin.admin_site.site_header,
        'site_title': admin.admin_site.site_title,
        'title': 'Список можливостей'
    }


class OpportunityDetail(LoginRequiredMixin, DetailView):
    model = models.Opportunity
    template_name = 'web/detail.html'
    extra_context = {
        'site_header': admin.admin_site.site_header,
        'site_title': admin.admin_site.site_title,
        'title': 'Детальна інформація'
    }
