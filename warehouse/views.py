from django.views import View
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from core.views import CreateView, UpdateView, ReadView
from core.html import badge
from product.models import Product, UnitOfMeasure

from warehouse.forms import (
    WarehouseTypeForm,
    WarehouseAddressForm,
    WarehouseForm,
    StorageBinForm,
    StockMovementForm,
    WarehouseTypeFilterForm,
    StockMovementFilterForm,
    StorageBinFilterForm,
    StockMovementInboundForm,
    StockMovementOutboundForm
)

from warehouse.models import (
    Warehouse,
    StorageBin,
    StockMovement,
    Stock
)

from warehouse.presenters import (
    WarehouseTypePresenter,
    StockMovementPresenter,
    StockPresenter,
    StorageBinPresenter,
    WarehousePresenter
)

from service.models import ServiceOrder
from purchase.models import PurchaseOrder


class Index(View):
    def get(self, request):
        return render(request, 'warehouse/index.html')


class CreateWarehouseType(CreateView):
    icon = 'icon_schema'
    form = WarehouseTypeForm
    redirect = 'warehouse:create_w_type'


class UpdateWarehouseType(UpdateView):
    icon = 'icon_schema'
    form = WarehouseTypeForm
    redirect = 'warehouse:update_w_type'


class ReadWarehouse(ReadView):
    model = WarehouseForm.Meta.model
    icon = 'icon_garage_home'
    redirect_for_new = 'warehouse:create_warehouse'
    redirect_for_edit = 'warehouse:read_warehouse'

    def get_presenters(self):
        return WarehousePresenter.all(order_by='name')


class ReadWarehouseType(ReadView):
    model = WarehouseTypeForm.Meta.model
    icon = 'icon_schema'
    redirect_for_new = 'warehouse:create_w_type'
    redirect_for_edit = 'warehouse:read_w_type'
    filter_form = WarehouseTypeFilterForm
    parameters = (
        'name',
        'description',
    )
    expressions = (
        'name__contains',
        'description__contains'
    )

    def get_presenters(self):
        return WarehouseTypePresenter.all(q_filter=self.get_filters(), order_by='name')

class CreateWarehouse(View):
    warehouse_form = WarehouseForm
    address_form = WarehouseAddressForm

    def get_context_data(self, warehouse_form, address_form):
        return {
            'warehouse_form': warehouse_form,
            'address_form': address_form,
            'page_title': _('New Warehouse'),
            'icon': 'icon_garage_home'
        }

    def get(self, request):
        context = self.get_context_data(self.warehouse_form, self.address_form)

        return render(request, 'warehouse/warehouse_form.html', context)

    def post(self, request):
        warehouse_form = self.warehouse_form(request.POST)
        address_form = self.address_form(request.POST)

        if warehouse_form.is_valid():
            warehouse = warehouse_form.save(commit=False)
            if address_form.is_valid():
                address = address_form.save()
                warehouse.address = address
                warehouse.save()

                messages.success(request, _('Save with success!'))
                return redirect('warehouse:create_warehouse')

        messages.error(request, _('Error: An error has occurred!'))
        context = self.get_context_data(warehouse_form, address_form)

        return render(request, 'warehouse/warehouse_form.html', context)


class UpdateWarehouse(View):
    warehouse_form = WarehouseForm
    address_form = WarehouseAddressForm

    def get_context_data(self, warehouse_form, address_form):
        return {
            'warehouse_form': warehouse_form,
            'address_form': address_form,
            'page_title': _('New Warehouse'),
            'icon': 'icon_garage_home'
        }

    def get(self, request, pk):
        warehouse = Warehouse.objects.get(pk=pk)
        warehouse_form = self.warehouse_form(instance=warehouse)
        address_form = self.address_form(instance=warehouse.address)
        context = self.get_context_data(warehouse_form, address_form)

        return render(request, 'warehouse/warehouse_form.html', context)

    def post(self, request, pk):
        warehouse = Warehouse.objects.get(pk=pk)
        warehouse_form = self.warehouse_form(request.POST, instance=warehouse)
        address_form = self.address_form(request.POST, instance=warehouse.address)

        if warehouse_form.is_valid():
            warehouse = warehouse_form.save(commit=False)
            if address_form.is_valid():
                address_form.save()
                warehouse.save()

                messages.success(request, _('Save with success!'))
                return redirect('warehouse:update_warehouse', warehouse.pk)

        messages.error(request, _('Error: An error has occurred!'))
        context = self.get_context_data(warehouse_form, address_form)

        return render(request, 'warehouse/warehouse_form.html', context)


class CreateStorageBin(CreateView):
    icon = 'icon_home_storage'
    form = StorageBinForm
    redirect = 'warehouse:create_storage_bin'


class UpdateStorageBin(UpdateView):
    icon = 'icon_home_storage'
    form = StorageBinForm
    redirect = 'warehouse:update_storage_bin'


class ReadStorageBin(ReadView):
    model = StorageBinForm.Meta.model
    icon = 'icon_home_storage'
    redirect_for_new = 'warehouse:create_storage_bin'
    redirect_for_edit = 'warehouse:read_storage_bin'
    filter_form = StorageBinFilterForm
    parameters = (
        'ref_position',
        'warehouse',
    )
    expressions = (
        'ref_position__contains',
        'warehouse__name__contains'
    )

    def get_presenters(self):
        return StorageBinPresenter.all(q_filter=self.get_filters() ,order_by='ref_position')


class StockMovementView(View):
    template: str
    page_title: str
    redirect: str
    session: str

    def get_context_data(self, form, stock_movement, form_general):
        return {
            'form': form,
            'stock_movement': stock_movement,
            'page_title': self.page_title,
            'icon': 'icon_inventory_2',
            'form_general': form_general
        }

    def get(self, request):
        form = StockMovementForm

        if request.session.get('service_order', ''):
            if self.session == 'stock_outbound':
                form_general = StockMovementOutboundForm(data={
                    'tax_invoice': request.session.get('tax_invoice', ''),
                    'service_order': self.get_service_order(
                        request.session.get('service_order', None).get('pk', '')
                    ),
                })
            else:
                form_general = StockMovementInboundForm(data={
                    'tax_invoice': request.session.get('tax_invoice', ''),
                    'purchase_order': self.get_purchase_order(
                        request.session.get('purchase_order', None).get('pk', '')
                    ),
                })
        else:
            if self.session == 'stock_outbound':
                form_general = StockMovementOutboundForm
            else:
                form_general = StockMovementInboundForm

        if request.session.get(self.session, ''):
            stock_movement = request.session[self.session]
        else:
            stock_movement = False

        return render(
            request,
            self.template,
            self.get_context_data(
                form,
                stock_movement,
                form_general
            )
        )

    def post(self, request):
        stock_movement_session = request.session[self.session]
        movements_list = []

        try:
            for movement in stock_movement_session:
                stock_movement = StockMovement(
                    date=movement['date'],
                    movement_type=movement['movement_type'],
                    item=self.get_item(movement['item']['pk']),
                    warehouse=self.get_warehouse(movement['warehouse']['pk']),
                    storage_bin=self.get_storage_bin(movement['storage_bin']['pk']),
                    quantity=movement['quantity']['qty'],
                    stock_uom=self.get_uom(movement['stock_uom']['pk']),
                    item_price=movement['item_price'],
                    service_order=self.get_service_order(
                        request.session.get('service_order', None).get('pk', '')),
                    purchase_order=self.get_purchase_order(
                        request.session.get('purchase_order', None).get('pk', '')),
                    tax_invoice=request.session.get('tax_invoice', None),
                )

                stock_movement.is_valid()
                movements_list.append(stock_movement)

            for stock_movement in movements_list:
                stock_movement.save()

            messages.success(
                request,
                _('Stock movement has been completed successfully.')
            )

            request.session.pop(self.session, None)
            request.session.pop('service_order', None)
            request.session.pop('tax_invoice', None)
            request.session.pop('purchase_order', None)

            return redirect('warehouse:read_stock_movements')

        except ValidationError as exc:
            messages.error(request, exc.message)
            return redirect(self.redirect)

    def get_item(self, pk):
        return Product.objects.get(pk=pk)

    def get_warehouse(self, pk):
        return Warehouse.objects.get(pk=pk)

    def get_storage_bin(self, pk):
        return StorageBin.objects.get(pk=pk)

    def get_uom(self, pk):
        return UnitOfMeasure.objects.get(pk=pk)

    def get_service_order(self, pk):
        if pk:
            return ServiceOrder.objects.get(pk=pk)
        return None

    def get_purchase_order(self, pk):
        if pk:
            return PurchaseOrder.objects.get(pk=pk)
        return None


class StockInbound(StockMovementView):
    template = 'warehouse/inbound.html'
    page_title = _('Stock Inbound')
    redirect = 'warehouse:stock_inbound'
    session = 'stock_inbound'


class StockOutbound(StockMovementView):
    template = 'warehouse/outbound.html'
    page_title = _('Stock Outbound')
    redirect = 'warehouse:stock_outbound'
    session = 'stock_outbound'


class StockSession(View):
    redirect: str
    session: str

    def post(self, request):
        request.session.setdefault(self.session, [])
        stock_movement = request.session[self.session]

        data = self.get_data_in_dic(request)

        if self.is_valid(data):
            stock_movement.append(data)
            request.session.modified = True

            request.session['service_order'] = self.get_service_order(request)
            request.session['tax_invoice'] = self.get_tax_invoice(request)
            request.session['purchase_order'] = self.get_purchase_order(request)

            return redirect(self.redirect)

        messages.error(
            request,
            _('Error: The storage bin you specified is not in the warehouse you specified.')
        )
        return redirect(self.redirect)

    def get_date(self, request):
        return request.POST['date']

    def get_movement_type(self, request):
        return request.POST['movement_type']

    def get_tax_invoice(self, request):
        tax_invoice = request.POST['tax_invoice']
        if tax_invoice:
            return tax_invoice
        return None

    def get_item(self, request):
        item = Product.objects.get(pk=request.POST['item'])

        return {
            'pk': str(item.pk),
            'description': str(item),
        }

    def get_warehouse(self, request):
        warehouse = Warehouse.objects.get(pk=request.POST['warehouse'])

        return {
            'pk': warehouse.pk,
            'description': str(warehouse),
        }

    def get_storage_bin(self, request):
        storage_bin = StorageBin.objects.get(pk=request.POST['storage_bin'])
        return {
            'pk': storage_bin.pk,
            'description': str(storage_bin),
        }

    def get_quantity(self, request):
        quantity = request.POST['quantity']
        stock = self.get_stock(request)
        if stock:
            color = 'success-100' if float(quantity) <= float(stock.quantity) else 'error-100'
            display = f"""<div>{quantity} / {badge(stock.quantity, color)}</div>"""
        else:
            display = f"""<div>{quantity}</div>"""
        return {
            'qty': quantity,
            'display': mark_safe(display),
        }

    def get_stock_uom(self, request):
        uom = UnitOfMeasure.objects.get(pk=request.POST['stock_uom'])
        return {
            'pk': str(uom.pk),
            'description': str(uom),
        }

    def get_item_price(self, request):
        price = request.POST['item_price']
        if price == '0':
            item = Product.objects.get(pk=request.POST['item'])
            price = str(item.price_cost)

        return price

    def get_service_order(self, request):
        pk = request.POST.get('service_order', '')

        if pk:
            service_order = ServiceOrder.objects.get(pk=pk)
            return {
                'pk': service_order.pk,
                'description': str(service_order)
            }

        return {
            'description': ''
        }

    def get_purchase_order(self, request):
        pk = request.POST.get('purchase_order', '')

        if pk:
            purchase_order = PurchaseOrder.objects.get(pk=pk)
            return {
                'pk': purchase_order.pk,
                'description': str(purchase_order)
            }

        return {
            'description': '' 
        }

    def get_stock(self, request):
        item = Product.objects.get(pk=request.POST['item'])
        storage_bin = StorageBin.objects.get(pk=request.POST['storage_bin'])
        stock_uom = UnitOfMeasure.objects.get(pk=request.POST['stock_uom'])

        if Stock.objects.filter(
                item=item,
                storage_bin=storage_bin,
                stock_uom=stock_uom
            ).exists():

            return Stock.objects.get(
                item=item,
                storage_bin=storage_bin,
                stock_uom=stock_uom
            )

        return 0

    def is_valid(self, data):
        storage_bin = StorageBin.objects.get(pk=data['storage_bin']['pk'])
        warehouse = Warehouse.objects.get(pk=data['warehouse']['pk'])

        return storage_bin.warehouse == warehouse

    def get_data_in_dic(self, request):
        return {
            'date': self.get_date(request),
            'movement_type': self.get_movement_type(request),
            'item': self.get_item(request),
            'warehouse': self.get_warehouse(request),
            'storage_bin': self.get_storage_bin(request),
            'quantity': self.get_quantity(request),
            'stock_uom': self.get_stock_uom(request),
            'item_price': self.get_item_price(request),
        }


class StockSessionClean(View):
    redirect: str
    session: str

    def get(self, request):
        request.session.pop(self.session, None)
        request.session.pop('service_order', None)
        request.session.pop('tax_invoice', None)

        return redirect(self.redirect)


class StockInboundSession(StockSession):
    redirect = 'warehouse:stock_inbound'
    session = 'stock_inbound'


class StockOutboundSession(StockSession):
    redirect = 'warehouse:stock_outbound'
    session = 'stock_outbound'


class StockInboundSessionClean(StockSessionClean):
    redirect = 'warehouse:stock_inbound'
    session = 'stock_inbound'


class StockOutboundSessionClean(StockSessionClean):
    redirect = 'warehouse:stock_outbound'
    session = 'stock_outbound'


class ReadStockMovements(ReadView):
    icon = 'icon_inventory'
    model = StockMovement
    redirect_for_new = 'warehouse:stock_inbound'
    filter_form = StockMovementFilterForm
    parameters = (
        'start_date',
        'end_date',
        'product_code',
        'movement_type',
    )
    expressions = (
        'date__date__gte',
        'date__date__lte',
        'item__sku_code',
        'movement_type',
    )

    def get_presenters(self):
        return StockMovementPresenter.all(q_filter=self.get_filters())


class ReadStock(ReadView):
    model = Stock
    icon = 'icon_inventory_2'
    redirect_for_new = 'warehouse:stock_inbound'

    def get_presenters(self):
        return StockPresenter.all()

class DeleteSessionStock(View):
    def get(self, request, index):
        if 'stock_outbound' in request.session:
            session = request.session['stock_outbound']

            try:
                del session[index]

                request.session['stock_outbound'] = session
            except IndexError:
                pass

        return redirect('warehouse:stock_outbound')
