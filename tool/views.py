from django.shortcuts import render
from django.views import View

from core.views import ReadView, CreateView, UpdateView
from tool.forms import (
    ToolCategoryForm,
    BrandForm,
    ToolForm,
    ToolDistributionRecordForm
)

from tool.presenters import (
    ToolCategoryPresenter,
    BrandPresenter,
    ToolPresenter,
    ToolDistributionRecordPresenter
)


class CreateToolCategory(CreateView):
    icon = 'icon_label'
    form = ToolCategoryForm
    redirect = 'tool:read_category'


class UpdateToolCategory(UpdateView):
    icon = 'icon_label'
    form = ToolCategoryForm
    redirect = 'tool:update_category'


class ReadToolCategory(ReadView):
    model = ToolCategoryForm.Meta.model
    icon = 'icon_label'
    redirect_for_new = 'tool:create_category'
    redirect_for_edit = 'tool:read_category'

    def get_presenters(self, request):
        return ToolCategoryPresenter.all(request)


class CreateBrand(CreateView):
    icon = 'icon_star'
    form = BrandForm
    redirect = 'tool:read_brand'


class UpdateBrand(UpdateView):
    icon = 'icon_star'
    form = BrandForm
    redirect = 'tool:update_brand'


class ReadBrand(ReadView):
    model = BrandForm.Meta.model
    icon = 'icon_star'
    redirect_for_new = 'tool:create_brand'
    redirect_for_edit = 'tool:read_brand'

    def get_presenters(self, request):
        return BrandPresenter.all(request)


class CreateTool(CreateView):
    icon = 'icon_build'
    form = ToolForm
    redirect = 'tool:read_tool'


class UpdateTool(UpdateView):
    icon = 'icon_build'
    form = ToolForm
    redirect = 'tool:update_tool'


class ReadTool(ReadView):
    model = ToolForm.Meta.model
    icon = 'icon_build'
    redirect_for_new = 'tool:create_tool'
    redirect_for_edit = 'tool:index'

    def get_presenters(self, request):
        return ToolPresenter.all(request)


class CreateToolDistributionRecord(CreateView):
    icon = 'icon_build'
    form = ToolDistributionRecordForm
    redirect = 'tool:read_distribution'


class UpdateToolDistributionRecord(UpdateView):
    icon = 'icon_build'
    form = ToolDistributionRecordForm
    redirect = 'tool:update_distribution'


class ReadToolDistributionRecord(ReadView):
    model = ToolDistributionRecordForm.Meta.model
    icon = 'icon_build'
    redirect_for_new = 'tool:create_distribution'
    redirect_for_edit = 'tool:read_distribution'

    def get_presenters(self, request):
        return ToolDistributionRecordPresenter.all(request)


class ToolIndex(View):
    def get(self, request):
        return render(request, 'tool/index.html')
