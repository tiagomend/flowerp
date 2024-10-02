from core.views import CreateView, UpdateView, ReadView

from service.forms import ServiceOrderForm
from service.presenters import ServiceOrderPresenter

class CreateServiceOrder(CreateView):
    icon = 'icon_engineering'
    form = ServiceOrderForm
    redirect = 'service:create_service_order'


class UpdateServiceOrder(UpdateView):
    icon = 'icon_engineering'
    form = ServiceOrderForm
    redirect = 'service:update_service_order'


class ReadServiceOrder(ReadView):
    model = ServiceOrderForm.Meta.model
    icon = 'icon_engineering'
    redirect_for_edit = 'service:read_service_order'
    redirect_for_new = 'service:create_service_order'

    def get_presenters(self):
        return ServiceOrderPresenter.all(order_by='-budget_number')
