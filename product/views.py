from core.views import CreateView, UpdateView, ReadView
from product.forms import ProductForm
from product.presenters import ProductPresenter


class CreateProduct(CreateView):
    form = ProductForm
    icon = 'icon_package_2'
    redirect = 'product:update_product'


class UpdateProduct(UpdateView):
    form = ProductForm
    icon = 'icon_package_2'
    redirect = 'product:update_product'

class ReadProduct(ReadView):
    icon = 'icon_package_2'
    redirect_for_new = 'product:create_product'
    redirect_for_edit = 'product:read_product'
    model = ProductForm.Meta.model

    def get_presenters(self):
        return ProductPresenter.all()
