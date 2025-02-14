from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.translation import gettext as _

from core.views import UpdateView, ReadView, CreateView

from purchase.models import PurchaseOrder, PurchaseOrderItems
from purchase.presenters import PurchaseOrderPresenter, SupplierPresenter

from purchase.forms import (
    PurchaseOrderForm,
    PurchaseOrderItemsForm,
    SupplierForm,
    ReportPOForm
)


class Index(View):
    def get(self, request):
        return render(request, 'purchase/index.html')


class StartPurchaseOrder(View):
    template = 'purchase/order_form.html'

    def get(self, request):
        form = PurchaseOrderForm
        purchase_items_form = PurchaseOrderItemsForm

        context = {
            'form': form,
            'purchase_items_form': purchase_items_form,
            'icon': 'icon_shopping_bag',
            'page_title': 'Nova Ordem de Compra',
            'start': True,
        }

        return render(request, self.template, context)

    def post(self, request):
        form = PurchaseOrderForm(request.POST)
        purchase_items_form = PurchaseOrderItemsForm(request.POST)

        context = {
            'form': form,
            'purchase_items_form': purchase_items_form,
            'icon': 'icon_shopping_bag',
            'page_title': 'Nova Ordem de Compra',
        }

        if purchase_items_form.is_valid():
            purchase_item = purchase_items_form.save(commit=False)
            if form.is_valid():
                purchase_order = form.save()
                purchase_item.purchase_order = purchase_order
                purchase_item.save()

            else:
                return render(request, self.template, context)

        else:
            return render(request, self.template, context)

        return redirect('purchase:purchase_order_view', purchase_order.id)


class PurchaseOrderView(View):
    template = 'purchase/order_form.html'

    def get(self, request, id):
        try:
            purchase_order = PurchaseOrder.objects.get(id=id)
        except ValidationError:
            purchase_order = PurchaseOrder.objects.get(pk=id)

        form = PurchaseOrderForm(instance=purchase_order)
        list_items = purchase_order.purchaseorderitems_set.all()
        purchase_items_form = PurchaseOrderItemsForm

        context = {
            'form': form,
            'purchase_items_form': purchase_items_form,
            'objects': list_items,
            'icon': 'icon_shopping_bag',
            'page_title': f'Ordem de Compra Nº: {purchase_order.code}',
            'url_delete': 'purchase:delete_purchase_item',
            'approved': purchase_order.is_approved(),
            'concluded': purchase_order.is_concluded(),
            'canceled': purchase_order.is_canceled(),
            'start': False,
        }

        return render(request, self.template, context)

    def post(self, request, id):
        try:
            purchase_order = PurchaseOrder.objects.get(id=id)
        except ValidationError:
            purchase_order = PurchaseOrder.objects.get(pk=id)

        form = PurchaseOrderForm(request.POST, instance=purchase_order)
        purchase_items_form = PurchaseOrderItemsForm(request.POST)

        if purchase_items_form.is_valid():
            purchase_item = purchase_items_form.save(commit=False)
            if form.is_valid():
                purchase_order = form.save()
                purchase_item.purchase_order = purchase_order
                purchase_item.save()

            else:
                print(form.errors)

        else:
            print(purchase_items_form.errors)

        return redirect('purchase:purchase_order_view', purchase_order.id)


class DeletePurchaseItem(View):
    def get(self, request, id):
        purchase_item = PurchaseOrderItems.objects.get(id=id)
        purchase_order = purchase_item.purchase_order

        if purchase_order.status == 'Draft':
            purchase_item.delete()
            messages.success(request, 'Linha excluída com sucesso!')

        else:
            messages.error(request, 'Linha não pode ser excluído!')

        return redirect('purchase:purchase_order_view', purchase_order.id)


class SavePurchaseOrder(View):
    def post(self, request, id):
        purchase_order = PurchaseOrder.objects.get(id=id)
        form = PurchaseOrderForm(request.POST, instance=purchase_order)

        if form.is_valid():
            form.save()
            messages.success(request, 'Ordem de Compra Salvo!')

            return redirect('purchase:purchase_order_view', purchase_order.id)


class ApprovePurchaseOrder(View):
    def post(self, request):
        purchase_order = PurchaseOrder.objects.get(id=request.POST['id'])
        purchase_order.approve()
        messages.success(request, 'Ordem de Compra Aprovada!')

        return redirect('purchase:purchase_order_view', purchase_order.id)


class ReceivePurchaseOrder(View):
    def post(self, request):
        purchase_order = PurchaseOrder.objects.get(id=request.POST['id'])
        stock_movement = purchase_order.receive_purchased_items()

        return redirect('stock:stock_inbound_view', stock_movement.id)


class CancelPurchaseOrder(View):
    def post(self, request):
        purchase_order = PurchaseOrder.objects.get(id=request.POST['id'])
        purchase_order.cancel()
        messages.success(request, 'Ordem de Compra Cancelada!')

        return redirect('purchase:purchase_order_view', purchase_order.id)


class ConcludePurchaseOrder(View):
    def post(self, request):
        purchase_order = PurchaseOrder.objects.get(id=request.POST['id'])
        purchase_order.conclude()
        messages.success(request, 'Ordem de Compra Concluída!')

        return redirect('purchase:purchase_order_view', purchase_order.id)


class UpdatePurchaseOrderItem(UpdateView):
    icon = 'icon_shopping_bag'
    form = PurchaseOrderItemsForm
    redirect = 'purchase:purchase_order_view'

    def post(self, request, pk):
        from core.exceptions import ErrorSavingModel

        model = self.form.Meta.model.objects.get(pk=pk)
        form = self.form(request.POST, instance=model)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, _('Save with success!'))
            except ErrorSavingModel as error:
                messages.error(request, error.message)

            return redirect(self.redirect, form.instance.purchase_order.id)

        messages.error(request, _('Error: An error has occurred!'))
        context = self.get_context_data(form=form, model=model)
        return render(request, 'global/form.html', context)


class ReadPurchaseOrder(ReadView):
    model = PurchaseOrder
    icon = 'icon_shopping_bag'
    redirect_for_new = 'purchase:start_purchase_order'
    redirect_for_edit = 'purchase:read_purchase_order'

    def get_presenters(self):
        return PurchaseOrderPresenter.all(order_by='-code')


class CreateSupplier(CreateView):
    icon = 'icon_location_home'
    form = SupplierForm
    redirect = 'purchase:read_supplier'


class UpdateSupplier(UpdateView):
    icon = 'icon_location_home'
    form = SupplierForm
    redirect = 'purchase:update_supplier'


class ReadSupplier(ReadView):
    icon = 'icon_location_home'
    model = SupplierForm.Meta.model
    redirect_for_new = 'purchase:create_supplier'
    redirect_for_edit = 'purchase:read_supplier'

    def get_presenters(self):
        return SupplierPresenter.all()


class ReportPurchaseOrder(View):
    def get(self, request):
        form = ReportPOForm
        context = {
            "form": form,
            "page_title": "Imprimir Grupo de Ordens de Compra",
            "icon": "icon_print"
        }
        return render(request, 'global/form.html', context)

    def post(self, request):
        if request.POST.get("code", "") != "":
            orders = PurchaseOrder.objects.filter(
                code=request.POST["code"]
            )
        else:
            orders = PurchaseOrder.objects.filter(
                approval_date__range=[
                    request.POST["start_date"],
                    request.POST["end_date"]
                ],
                status__in=["Approved"]
            )

        totals = 0

        for order in orders:
            totals += order.calculate_total()

        context = {
            "orders": orders,
            "page_title": "Imprimir Grupo de Ordens de Compra",
            "icon": "icon_print",
            "totals": f"R$ {round(totals, 2)}".replace('.', ',')
        }

        return render(request, 'purchase/order_report.html', context)
