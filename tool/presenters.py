from django.utils.translation import gettext as _

from core.presenters import Presenter

from tool.models import ToolCategory, Brand, Tool, ToolDistributionRecord

class ToolCategoryPresenter(Presenter):
    model = ToolCategory

    @property
    def values(self):
        return [
            self.model.name
        ]

    @property
    def headers(self):
        return [
            _('Name')
        ]


class BrandPresenter(Presenter):
    model = Brand

    @property
    def values(self):
        return [
            self.model.name
        ]

    @property
    def headers(self):
        return [
            _('Name')
        ]


class ToolPresenter(Presenter):
    model = Tool

    @property
    def values(self):
        return [
            self.model.item.name,
            self.model.asset_number,
            self.model.serial_number,
            self.model.acquisition_date,
            self.model.brand,
            self.model.get_tool_status_display(),
        ]

    @property
    def headers(self):
        return [
            _('Name'),
            _('Asset number'),
            _('Serial number'),
            _('Acquisition date'),
            _('Brand'),
            _('Tool status'),
        ]


class ToolDistributionRecordPresenter(Presenter):
    model = ToolDistributionRecord

    @property
    def values(self):
        return_date = self.model.return_date

        return [
            self.model.tool,
            self.model.employee,
            self.model.issue_date,
            return_date if return_date else ''
        ]

    @property
    def headers(self):
        return [
            _('Tool'),
            _('Employee'),
            _('Issue date'),
            _('Return date'),
        ]
