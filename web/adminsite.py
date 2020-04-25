from django.apps import apps
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from django.contrib.admin import AdminSite, site


class OrderedAdminSite(AdminSite):
    admin_order = ()

    def __init__(self, name='admin', **kwargs):
        """
        Set any site attributes in __init__() and register/unregister models
        """
        super().__init__(name)
        # Copy registered models from django.contrib.admin.site
        self._registry.update(site._registry)
        for k, v in kwargs.items():
            if k == 'register':
                self.register(v)
            elif k == 'unregister':
                self.unregister(v)
            else:
                setattr(self, k, v)

    @staticmethod
    def sortfn(order, item, verbose_name=None):
        """
        Sort key function - use index of item in order if exists,
        otherwise item (alphabetically by name or object_name)
        """
        verbose_name = item if verbose_name is None else verbose_name
        return (order.index(item), 0) if item in order else (len(order), verbose_name)

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)

        ordered_apps = tuple(a[0] for a in self.admin_order)

        # Sort the app list
        app_list = sorted(app_dict.values(), key=lambda app: self.sortfn(
            ordered_apps, app['app_label']))

        # Sort the models within each app.
        for i, app in enumerate(app_list):
            if app['app_label'] in ordered_apps:
                # Try to sort by settings (self.admin_order)
                app['models'].sort(key=lambda model: self.sortfn(
                    self.admin_order[i][1],
                    model['object_name'],
                    model['name']))
            else:
                # Sort the models alphabetically
                app['models'].sort(key=lambda x: x['name'])

        return app_list

    def app_index(self, request, app_label, extra_context=None):
        """
        Display the app admin index page.
        """
        app_dict = self._build_app_dict(request, app_label)
        if not app_dict:
            raise Http404('The requested admin page does not exist.')

        # Sort the models within the app
        ordered_apps = tuple(a[0] for a in self.admin_order)
        if app_label in ordered_apps:
            # Try to sort by settings (self.admin_order)
            app_dict['models'].sort(key=lambda model: self.sortfn(
                self.admin_order[ordered_apps.index(app_label)][1],
                model['object_name'],
                model['name']))
        else:
            # Sort the models alphabetically
            app_dict['models'].sort(key=lambda x: x['name'])
        app_name = apps.get_app_config(app_label).verbose_name
        context = {
            **self.each_context(request),
            'title': _('%(app)s administration') % {'app': app_name},
            'app_list': [app_dict],
            'app_label': app_label,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request, self.app_index_template or [
            'admin/%s/app_index.html' % app_label,
            'admin/app_index.html'
        ], context)
