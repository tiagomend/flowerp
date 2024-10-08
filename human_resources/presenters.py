from datetime import datetime

from django.utils.translation import gettext as _

from core.presenters import Presenter
from core.html import badge

from human_resources.models import (
    EmployeePosition,
    Employee,
    EmployeeHiring,
    Vacation,
    Salary,
    SalaryAdjustment,
    Document
)

def days_between(target_date):
    today = datetime.now().date()
    if isinstance(target_date, str):
        target_date = datetime.strptime(target_date, '%Y-%m-%d').date()

    delta = target_date - today
    return delta.days

class EmployeePositionPresenter(Presenter):
    model = EmployeePosition

    @property
    def values(self):
        return [self.model.name]

    @property
    def headers(self):
        return [_('Name')]


class EmployeePresenter(Presenter):
    model = Employee

    @property
    def values(self):
        return [
            self.model.pis_number,
            self.model,
            self.model.position,
        ]

    @property
    def headers(self):
        return [
            _('Pis Number'),
            _('Name'),
            _('Position'),
        ]


class EmployeeHiringPresenter(Presenter):
    model = EmployeeHiring

    @property
    def values(self):

        return [
            self.model.employee.pis_number,
            self.model.employee,
            self.model.salary.display_position(),
            self.model.salary.display_salary(),
            self.model.enterprise,
            self.format_date(self.model.admission_date),
            self.format_date(self.model.expiry_of_experience),
            self.format_date(self.model.termination_date),
        ]

    @property
    def headers(self):
        return [
            _('Pis number'),
            _('Name'),
            _('Position'),
            _('Salary'),
            _('Enterprise'),
            _('Admission date'),
            _('Expiry of experience'),
            _('Termination date'),
        ]

    def format_date(self, date_obj):
        if date_obj:
            return date_obj.strftime('%d/%m/%Y')
        return ''


class VacationExpirationPresenter(Presenter):
    model = EmployeeHiring

    @property
    def values(self):
        between = days_between(self.model.grant_limit) if \
            self.model.grant_limit else ''

        if not between:
            grant_limit = ''

        elif between <= 15:
            grant_limit = badge(
                self.model.grant_limit.strftime('%d/%m/%Y'),
                'error-100'
            )
        elif between > 15:
            grant_limit = badge(
                self.model.grant_limit.strftime('%d/%m/%Y'),
                'success-100'
            )

        between = days_between(self.model.vacation_expiration_date) if \
            self.model.vacation_expiration_date else ''

        if not between:
            vacation_expiration_date = ''

        elif between <= 15:
            vacation_expiration_date = badge(
                self.model.vacation_expiration_date.strftime('%d/%m/%Y'),
                'error-100'
            )
        elif between > 15:
            vacation_expiration_date = badge(
                self.model.vacation_expiration_date.strftime('%d/%m/%Y'),
                'success-100'
            )

        return [
            self.model.employee,
            self.model.enterprise,
            self.model.get_paid_off(),
            vacation_expiration_date,
            grant_limit,
        ]

    @property
    def headers(self):
        return [
            _('Name'),
            _('Enterprise'),
            _('Paid off'),
            _('Vacation Expiration Date'),
            _('Grant Limit'),
        ]


class VacationPresenter(Presenter):
    model = Vacation

    @property
    def values(self):
        between = days_between(self.model.employee_hiring.grant_limit) if \
            self.model.employee_hiring.grant_limit else ''

        if not between:
            grant_limit = ''

        elif between <= 15:
            grant_limit = badge(
                self.model.employee_hiring.grant_limit.strftime('%d/%m/%Y'),
                'error-100'
            )
        elif between > 15:
            grant_limit = badge(
                self.model.employee_hiring.grant_limit.strftime('%d/%m/%Y'),
                'success-100'
            )

        between = days_between(self.model.employee_hiring.vacation_expiration_date) if \
            self.model.employee_hiring.vacation_expiration_date else ''

        if not between:
            vacation_expiration_date = ''

        elif between <= 15:
            vacation_expiration_date = badge(
                self.model.employee_hiring.vacation_expiration_date.strftime('%d/%m/%Y'),
                'error-100'
            )
        elif between > 15:
            vacation_expiration_date = badge(
                self.model.employee_hiring.vacation_expiration_date.strftime('%d/%m/%Y'),
                'success-100'
            )
        return [
            self.model.employee_hiring,
            vacation_expiration_date,
            grant_limit,
            self.model.paid_off,
            self.model.start_date,
            self.model.end_date,
        ]

    @property
    def headers(self):
        return [
            _('Name'),
            _('Vacation Expiration Date'),
            _('Vacation limit'),
            _('Paid off'),
            _('Start date'),
            _('End date'),
        ]


class SalaryPresenter(Presenter):
    model = Salary

    @property
    def values(self):
        return [
            self.model.display_position(),
            self.model.get_modality_display(),
            self.model.base_salary
        ]

    @property
    def headers(self):
        return [
            _('Position'),
            _('Modality'),
            _('Base Salary')
        ]


class SalaryAdjustmentPresenter(Presenter):
    model = SalaryAdjustment

    @property
    def values(self):
        return [
            self.model.date,
            self.model.salary.display_position(),
            self.model.previous_salary,
            self.model.get_adjustment_type_display(),
            self.model.adjustment_value,
        ]

    @property
    def headers(self):
        return [
            _('Date'),
            _('Position'),
            _('Previous Salary'),
            _('Adjustment Type'),
            _('Adjustment Value')
        ]


class DocumentPresenter(Presenter):
    model = Document

    @property
    def values(self):
        between = days_between(self.model.expiration_date) if self.model.expiration_date else ''

        if not between:
            expiration_date = ''

        elif between <= 15:
            expiration_date = badge(
                self.model.expiration_date.strftime('%d/%m/%Y'),
                'error-100'
            )
        elif between > 15:
            expiration_date = badge(
                self.model.expiration_date.strftime('%d/%m/%Y'),
                'success-100'
            )

        return [
            self.model.name,
            self.model.employee_hiring,
            self.model.issue_date if self.model.issue_date else '',
            expiration_date,
        ]

    @property
    def headers(self):
        return [
            _('Document Name'),
            _('Employee Name'),
            _('Issue date'),
            _('Expiration date'),
        ]
