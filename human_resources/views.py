from datetime import date, time, timedelta
import json

from django.views import View
from django.http import FileResponse, Http404, JsonResponse
from django.views.generic.edit import CreateView as CreateViewDjango
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib import messages
from django.utils.translation import gettext as _

from core.views import CreateView, UpdateView, ReadView
from core.utils import format_decimal_to_hours

from human_resources.forms import (
    EmployeePositionForm,
    EmployeeForm,
    EmployeeHiringForm,
    EmployeeHiringEditForm,
    VacationForm,
    SalaryForm,
    SalaryAdjustmentForm,
    DocumentForm
)
from human_resources.presenters import (
    EmployeePositionPresenter,
    EmployeePresenter,
    EmployeeHiringPresenter,
    VacationPresenter,
    SalaryPresenter,
    SalaryAdjustmentPresenter,
    DocumentPresenter
)
from human_resources.models import (
    Employee,
    EmployeeHiring,
    Point,
    Observation,
    Holiday,
    Document
)


class CreateEmployeePosition(CreateView):
    icon = 'icon_schema'
    form = EmployeePositionForm
    redirect = 'human_resources:create_position'


class UpdateEmployeePosition(UpdateView):
    icon = 'icon_schema'
    form = EmployeePositionForm
    redirect = 'human_resources:update_position'


class ReadEmployeePosition(ReadView):
    model = EmployeePositionForm.Meta.model
    icon = 'icon_schema'
    redirect_for_new = 'human_resources:create_position'
    redirect_for_edit = 'human_resources:read_position'

    def get_presenters(self):
        return EmployeePositionPresenter.all('name')


class CreateEmployee(CreateView):
    icon = 'icon_badge'
    form = EmployeeForm
    redirect = 'human_resources:create_employee'


class UpdateEmployee(UpdateView):
    icon = 'icon_badge'
    form = EmployeeForm
    redirect = 'human_resources:update_employee'


class ReadEmployee(ReadView):
    icon = 'icon_badge'
    model = EmployeeForm.Meta.model
    redirect_for_new = 'human_resources:create_employee'
    redirect_for_edit = 'human_resources:read_employee'

    def get_presenters(self):
        return EmployeePresenter.all('first_name')


class CreateEmployeeHiring(CreateView):
    icon = 'icon_badge'
    form = EmployeeHiringForm
    redirect = 'human_resources:create_hiring'


class UpdateEmployeeHiring(UpdateView):
    icon = 'icon_badge'
    form = EmployeeHiringEditForm
    redirect = 'human_resources:update_hiring'


class ReadEmployeeHiring(ReadView):
    icon = 'icon_badge'
    model = EmployeeHiringForm.Meta.model
    redirect_for_new = 'human_resources:create_hiring'
    redirect_for_edit = 'human_resources:read_hiring'

    def get_presenters(self):
        return EmployeeHiringPresenter.all('employee__first_name')


class CreateVacation(CreateView):
    icon = 'icon_event_available'
    form = VacationForm
    redirect = 'human_resources:create_vacation'


class UpdateVacation(UpdateView):
    icon = 'icon_event_available'
    form = VacationForm
    redirect = 'human_resources:update_vacation'


class ReadVacation(ReadView):
    icon = 'icon_event_available'
    model = VacationForm.Meta.model
    redirect_for_new = 'human_resources:create_vacation'
    redirect_for_edit = 'human_resources:read_vacation'

    def get_presenters(self):
        return VacationPresenter.all()


class RegisterPointHenryPrisma(View):
    def get_context_data(self):
        context = {
            'page_title': 'Point Register',
            'icon': 'icon_more_time'
        }

        return context

    def get(self, request):
        context = self.get_context_data()

        return render(request, 'human_resources/point-register.html', context)

    def post(self, request):
        self.save_file(request.FILES.get('point_henry'))
        self.register()
        context = self.get_context_data()
        messages.success(request, 'Time clock data was processed successfully!')

        return render(request, 'human_resources/point-register.html', context)

    def save_file(self, file):
        with open('human_resources/point.txt', 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

    def register(self):
        file = open('human_resources/point.txt', 'r')

        for line in file:
            if self.is_time_stamp_event(line):
                pis_number = self.get_employee_pis(line)

                if self.is_there_an_employee(pis_number):
                    date_field = self.get_date(line)
                    time_field = self.get_time(line)

                    if not Point.is_there_time_sheet(self.employee_hiring, date_field):
                        Point.create_time_sheet(
                            self.employee_hiring,
                            self.get_month(line),
                            self.get_year(line)
                        )

                    point = Point.objects.get(
                        employee_hiring=self.employee_hiring,
                        date=date_field
                    )

                    if not point.this_point_existis(time_field):
                        self.point_out(point, time_field)
                    else:
                        continue
                else:
                    continue
            else:
                continue

    def is_time_stamp_event(self, line):
        EVENT_NUMBER = '3'
        return line[9:10] is EVENT_NUMBER

    def get_employee_pis(self, line):
        return line[23:34]

    def get_point(self, line):
        return time(int(line[18:20]), int(line[20:22]))

    def get_year(self, line):
        return int(line[14:18])

    def get_month(self, line):
        return int(line[12:14])

    def get_day(self, line):
        return int(line[10:12])

    def get_date(self, line):
        year = self.get_year(line)
        month = self.get_month(line)
        day = self.get_day(line)
        return date(year, month, day)

    def get_time(self, line):
        hour = int(line[18:20])
        minute = int(line[20:22])

        return time(hour, minute)

    def is_there_an_employee(self, pis_number):
        if not Employee.objects.filter(pis_number=pis_number).exists():
            return False

        employee = Employee.objects.get(pis_number=pis_number)

        if not EmployeeHiring.objects.filter(
            employee=employee,
            termination_date__isnull=True
        ).exists():
            return False

        self.employee_hiring = EmployeeHiring.objects.get(
            employee=employee,
            termination_date__isnull=True
        )
        return True

    def point_out(self, point, time_field):
        zero_hours = time(0)

        if point.first_entry == zero_hours:
            point.first_entry = time_field
            point.save()

        elif point.first_exit == zero_hours:
            point.first_exit = time_field
            point.save()

        elif point.second_entry == zero_hours:
            point.second_entry = time_field
            point.save()

        elif point.second_exit == zero_hours:
            point.second_exit = time_field
            point.save()

        elif point.third_entry == zero_hours:
            point.third_entry = time_field
            point.save()

        elif point.third_exit == zero_hours:
            point.third_exit = time_field
            point.save()


class TimeSheetService:
    def __init__(self, employee_hiring, month_year) -> None:
        self.employee_hiring = employee_hiring
        self.month_year = month_year

    def get_month(self):
        return int(self.month_year[5:7])

    def get_year(self):
        return int(self.month_year[0:4])

    def get_time_sheet(self):
        _date = date(self.get_year(), self.get_month(), 1)
        if not Point.is_there_time_sheet(self.employee_hiring, _date):
            Point.create_time_sheet(self.employee_hiring, self.get_month(), self.get_year())

        self.points = Point.objects.filter(
            date__year=self.get_year(),
            date__month=self.get_month(),
            employee_hiring=self.employee_hiring
        ).order_by('date')

        return self.points

    def get_observations(self):
        observations = []

        for point in self.points:
            observations_model = Observation.objects.filter(point=point)
            for observation in observations_model:
                observations.append(observation)

        return observations

    def is_fifty_per_center(self, point):
        return point.date.strftime('%A') == 'Saturday'

    def is_hundred_per_center(self, point):
        is_sunday = point.date.strftime('%A') == 'Sunday'
        is_holiday = Holiday.objects.filter(
            day=point.date.day,
            month=point.date.month
        ).exists()

        return is_sunday or is_holiday

    def calculate_total(self):
        total_hours = timedelta(seconds=0)

        for point in self.points:
            total_hours += point.total_hours
        return total_hours.total_seconds() / 3600

    def total_fifty_per_center(self):
        total = timedelta(seconds=0)
        for point in self.points:
            if not self.is_hundred_per_center(point):
                total_hours = point.total_hours
                if self.is_fifty_per_center(point):
                    total += total_hours

                # TODO: this implementation must be overridden to use the WorkingHours model
                elif total_hours >= timedelta(hours=9, minutes=0, seconds=0):
                    total += total_hours - timedelta(hours=8, minutes=45, seconds=0)
        return total.total_seconds() / 3600

    def total_hundred_per_center(self):
        total = timedelta(seconds=0)

        for point in self.points:
            if self.is_hundred_per_center(point):
                total += point.total_hours
        return total.total_seconds() / 3600

    def total_normal_hours(self):
        return ((self.calculate_total() - \
                self.total_hundred_per_center()) - \
                self.total_fifty_per_center())


class TimeSheetReport(View):
    def get(self, request):
        employees = EmployeeHiring.objects.filter(termination_date__isnull=True)

        context = {
            'employees': employees
        }

        if request.GET:
            pk_employee: str = request.GET.get('employee_hiring', '')
            month_year = request.GET.get('month_year', '')

            if pk_employee.isnumeric():
                employee = EmployeeHiring.objects.get(pk=pk_employee)
                service = TimeSheetService(employee, month_year)
                time_sheet = service.get_time_sheet()
                context['normal_hours'] = format_decimal_to_hours(
                        service.total_normal_hours()
                    )

                context['fifty_percent_hours'] = format_decimal_to_hours(
                        service.total_fifty_per_center()
                    )

                context['hundred_percent_hours'] = format_decimal_to_hours(
                        service.total_hundred_per_center()
                    )

                context['time_sheet'] = time_sheet
                context['month_year'] = month_year
                context['pk_employee'] = pk_employee

        return render(request, 'human_resources/time_sheet.html', context)


class TimeSheetEdit(View):
    def get(self, request, employee_hiring, month_year):

        employee = EmployeeHiring.objects.get(pk=employee_hiring)
        service = TimeSheetService(employee, month_year)
        time_sheet = service.get_time_sheet()
        context = {'time_sheet': time_sheet}

        return render(request, 'human_resources/time_sheet_edit.html', context)

    def post(self, request, employee_hiring, month_year):
        employee = EmployeeHiring.objects.get(pk=employee_hiring)
        data = json.loads(request.body)
        print(month_year)

        for value in data:
            date_request = value[0]['date']
            date_instance = date(
                self.get_year(date_request),
                self.get_month(date_request),
                self.get_day(date_request)
            )
            point = Point.objects.get(employee_hiring=employee, date=date_instance)
            point.first_entry = value[0]['first_entry']
            point.first_exit = value[0]['first_exit']
            point.second_entry = value[0]['second_entry']
            point.second_exit = value[0]['second_exit']
            point.third_entry = value[0]['third_entry']
            point.third_exit = value[0]['third_exit']
            point.save()

        message = _('Save with success!')

        return JsonResponse({'msg': message}, status=200)

    def get_month(self, date_request):
        return int(date_request[3:5])

    def get_year(self, date_request):
        return int(date_request[6:])

    def get_day(self, date_request):
        return int(date_request[0:2])


class CreateSalary(CreateView):
    icon = 'icon_account_balance_wallet'
    form = SalaryForm
    redirect = 'human_resources:create_salary'


class UpdateSalary(UpdateView):
    icon = 'icon_account_balance_wallet'
    form = SalaryForm
    redirect = 'human_resources:update_salary'


class ReadSalary(ReadView):
    icon = 'icon_account_balance_wallet'
    model = SalaryForm.Meta.model
    redirect_for_new = 'human_resources:create_salary'
    redirect_for_edit = 'human_resources:read_salary'

    def get_presenters(self):
        return SalaryPresenter.all('position__name')


class CreateSalaryAdjustment(CreateView):
    icon = 'icon_account_balance_wallet'
    form = SalaryAdjustmentForm
    redirect = 'human_resources:create_salary_adjustment'


class UpdateSalaryAdjustment(UpdateView):
    icon = 'icon_account_balance_wallet'
    form = SalaryAdjustmentForm
    redirect = 'human_resources:update_salary_adjustment'


class ReadSalaryAdjustment(ReadView):
    icon = 'icon_account_balance_wallet'
    model = SalaryAdjustmentForm.Meta.model
    redirect_for_new = 'human_resources:create_salary_adjustment'
    redirect_for_edit = 'human_resources:read_salary_adjustment'

    def get_presenters(self):
        return SalaryAdjustmentPresenter.all()


class CreateDocument(CreateViewDjango):
    model = Document
    form_class = DocumentForm
    template_name = 'global/form.html'
    success_url = reverse_lazy('human_resources:read_document')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enctype'] = True
        context['icon'] = 'icon_attach_file'
        context['page_title'] = 'New Document'
        return context


class ReadDocument(ReadView):
    icon = 'icon_attach_file'
    model = Document
    template = 'human_resources/document_read.html'
    redirect_for_new = 'human_resources:create_document'
    redirect_for_edit = 'human_resources:read_document'

    def get_presenters(self):
        return DocumentPresenter.all()


def view_document(_, document_id):
    try:
        document = Document.objects.get(pk=document_id)
        return FileResponse(document.file.open(), content_type='application/pdf')
    except Document.DoesNotExist:
        raise Http404("Document not found") from Document.DoesNotExist


class HumanResourcesIndex(View):
    def get(self, request):
        return render(request, 'human_resources/index.html')
