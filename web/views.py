from django.conf import settings
from django.http import JsonResponse
from django.views.generic import View, TemplateView, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscribed'] = self.request.user.subs.filter(id=self.get_object().id).exists()
        #context['subscribed'] = self.get_object().students.filter(id=self.request.user.id).exists()
        return context


class ApiNew(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            if request.POST['token'] == getattr(settings, "BOT_TOKEN", None):
                profile = models.Profile.objects.create(
                    email=request.POST['email'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    role=request.POST['role'],
                    city=request.POST['city']
                )
                JsonResponse({'ok': profile.id})
            else:
                return JsonResponse({'error': 'Incorrect token'})
        except:
            return JsonResponse({'error': 'Incorrect request'})


class ApiSubscribe(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            profile = models.Profile.objects.get(id=request.POST.get('id'))
            opp = models.Opportunity.objects.get(id=request.POST.get('opp'))
            profile.subs.add(opp)
            return JsonResponse({'ok': f"{profile.id}+{opp.id}"})
        except:
            return JsonResponse({'error': 'Incorrect request'})
