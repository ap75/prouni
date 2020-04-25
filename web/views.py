from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from . import models, admin, tables, filters


class IndexView(TemplateView):
    template_name = 'web/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'site_header': admin.admin_site.site_header,
            'site_title': admin.admin_site.site_title,
            'title': 'Це головна сторінка'
        })
        return context


class OpportunityList(SingleTableMixin, LoginRequiredMixin, FilterView):
    template_name = 'web/list.html'
    table_class = tables.OpportunityTable
    filterset_class = filters.OpportunityFilter
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'site_header': admin.admin_site.site_header,
            'site_title': admin.admin_site.site_title,
            'title': 'Список можливостей'
        })
        return context
