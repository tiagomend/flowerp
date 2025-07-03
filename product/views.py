from core.views import CreateView, UpdateView, ReadView
from product.forms import (
    ProductForm,
    UnitOfMeasureForm,
    ProductCategoryForm,
    ItemTypeForSpedForm,
    ProductFilterForm
)
from product.presenters import (
    ProductPresenter,
    UnitOfMeasurePresenter,
    ProductCategoryPresenter,
    ItemTypeForSpedPresenter
)


class CreateProduct(CreateView):
    form = ProductForm
    icon = 'icon_package_2'
    redirect = 'product:read_product'


class UpdateProduct(UpdateView):
    form = ProductForm
    icon = 'icon_package_2'
    redirect = 'product:update_product'

class ReadProduct(ReadView):
    icon = 'icon_package_2'
    redirect_for_new = 'product:create_product'
    redirect_for_edit = 'product:read_product'
    model = ProductForm.Meta.model
    filter_form = ProductFilterForm
    parameters = (
        'name',
        'code',
    )
    expressions = (
        'name__contains',
        'sku_code__contains'
    )

    def get_presenters(self, request):
        return ProductPresenter.all(
            request=request,
            q_filter=self.get_filters(),
            order_by=('sku_code')
        )


class CreateUnitOfMeasure(CreateView):
    form = UnitOfMeasureForm
    icon = 'icon_package_2'
    redirect = 'product:read_uom'


class UpdateUnitOfMeasure(UpdateView):
    form = UnitOfMeasureForm
    icon = 'icon_package_2'
    redirect = 'product:update_uom'


class ReadUnitOfMeasure(ReadView):
    icon = 'icon_package_2'
    redirect_for_new = 'product:create_uom'
    redirect_for_edit = 'product:read_uom'
    model = UnitOfMeasureForm.Meta.model

    def get_presenters(self, request):
        return UnitOfMeasurePresenter.all(request)


class CreateProductCategory(CreateView):
    form = ProductCategoryForm
    icon = 'icon_package_2'
    redirect = 'product:read_category'


class UpdateProductCategory(UpdateView):
    form = ProductCategoryForm
    icon = 'icon_package_2'
    redirect = 'product:update_category'


class ReadProductCategory(ReadView):
    icon = 'icon_package_2'
    redirect_for_new = 'product:create_category'
    redirect_for_edit = 'product:read_category'
    model = ProductCategoryForm.Meta.model

    def get_presenters(self, request):
        return ProductCategoryPresenter.all(request)


class CreateItemTypeForSped(CreateView):
    form = ItemTypeForSpedForm
    icon = 'icon_package_2'
    redirect = 'product:read_item_type'


class UpdateItemTypeForSped(UpdateView):
    form = ItemTypeForSpedForm
    icon = 'icon_package_2'
    redirect = 'product:update_item_type'


class ReadItemTypeForSped(ReadView):
    icon = 'icon_package_2'
    redirect_for_new = 'product:create_item_type'
    redirect_for_edit = 'product:read_item_type'
    model = ItemTypeForSpedForm.Meta.model

    def get_presenters(self, request):
        return ItemTypeForSpedPresenter.all(request, order_by='-code')
