from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import translation
from django.utils.translation import gettext as _

from core.forms import EnterpriseForm, CoustCenterForm
from core.presenters import EnterprisePresenter, CoustCenterPresenter
from core.exceptions import ErrorSavingModel

class CreateView(View):
    form: ModelForm
    redirect: str
    icon: str

    def get_context_data(self, **kwargs):
        new = _('New')
        verbose_name = self.form.Meta.model._meta.verbose_name
        context = {
            'page_title': f'{new} {verbose_name}'
        }
        context['form'] = kwargs['form']
        context['icon'] = self.icon
        html_language = translation.get_language()
        context['html_language'] = html_language

        return context

    def get(self, request):
        form = self.form
        context = self.get_context_data(form=form)
        return render(request, 'global/form.html', context)

    def post(self, request):
        form = self.form(request.POST)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, _('Save with success!'))
                return redirect(self.redirect)

            except ValidationError as error:
                messages.error(request, error.message)
                context = self.get_context_data(form=form)
                return render(request, 'global/form.html', context)

        context = self.get_context_data(form=form)
        messages.error(request, _('Error: An error has occurred!'))
        return render(request, 'global/form.html', context)


class UpdateView(View):
    form: ModelForm
    redirect: str
    icon: str

    def get_context_data(self, **kwargs):
        context = {
            'page_title': f'{self.form.Meta.model._meta.verbose_name}: {kwargs["model"]}'
        }
        context['form'] = kwargs['form']
        context['icon'] = self.icon
        html_language = translation.get_language()
        context['html_language'] = html_language

        return context

    def get(self, request, pk):
        model = self.form.Meta.model.objects.get(pk=pk)
        form = self.form(instance=model)
        context = self.get_context_data(form=form, model=model)
        return render(request, 'global/form.html', context)

    def post(self, request, pk):
        model = self.form.Meta.model.objects.get(pk=pk)
        form = self.form(request.POST, instance=model)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, _('Save with success!'))
            except ErrorSavingModel as error:
                messages.error(request, error.message)

            return redirect(self.redirect, form.instance.pk)

        messages.error(request, _('Error: An error has occurred!'))
        context = self.get_context_data(form=form, model=model)
        return render(request, 'global/form.html', context)


class ReadView(View):
    presenters: list
    icon: str
    redirect_for_new: str
    redirect_for_edit = False
    model: object
    template = 'global/read.html'
    page_title = ''
    filter_form = None

    def get_context_data(self):
        list_of = _('List of')

        if self.page_title:
            context = {
                'page_title': self.page_title
            }
        else:
            context = {
                'page_title': f'{list_of} {self.model._meta.verbose_name}'
            }

        context['presenters'] = self.get_presenters()
        context['icon'] = self.icon
        context['redirect_for_new'] = reverse_lazy(self.redirect_for_new)

        if self.redirect_for_edit:
            context['redirect_for_edit'] = reverse_lazy(self.redirect_for_edit)

        html_language = translation.get_language()
        context['html_language'] = html_language

        if self.filter_form:
            context['filter_form'] = self.filter_form

        return context

    def get_filters(self):
        if self.parameters:
            filters = Q()
            for i, parameter in enumerate(self.parameters):
                search = self.request.GET.get(parameter, '')

                if search:
                    args = {f"{self.expressions[i]}": search}
                    filters &= Q(**args)

            return filters
        return None

    def get_presenters(self):
        raise NotImplementedError

    def get(self, request):
        context = self.get_context_data()

        return render(request, self.template, context)


class CreateEnterprise(CreateView):
    form = EnterpriseForm
    icon = 'icon_location_home'
    redirect = 'core:read_enterprise'


class UpdateEnterprise(UpdateView):
    form = EnterpriseForm
    icon = 'icon_location_home'
    redirect = 'core:update_enterprise'


class ReadEnterprise(ReadView):
    icon = 'icon_location_home'
    model = EnterpriseForm.Meta.model
    redirect_for_new = 'core:create_enterprise'
    redirect_for_edit = 'core:read_enterprise'

    def get_presenters(self):
        return EnterprisePresenter.all()


class CreateCoustCenter(CreateView):
    form = CoustCenterForm
    icon = 'icon_location_home'
    redirect = 'core:read_coustcenter'


class UpdateCoustCenter(UpdateView):
    form = CoustCenterForm
    icon = 'icon_location_home'
    redirect = 'core:update_coustcenter'


class ReadCoustCenter(ReadView):
    icon = 'icon_location_home'
    model = CoustCenterForm.Meta.model
    redirect_for_new = 'core:create_coustcenter'
    redirect_for_edit = 'core:read_coustcenter'

    def get_presenters(self):
        return CoustCenterPresenter.all()