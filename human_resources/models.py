from calendar import TextCalendar
import os
import uuid
import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.exceptions import ErrorSavingModel


class ActiveEmployeeHiring(ErrorSavingModel):
    pass

class NoLimitConcession(ErrorSavingModel):
    pass


class EmployeePosition(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = _('Employee Position')


class Salary(models.Model):
    position = models.ForeignKey(
        EmployeePosition,
        on_delete=models.PROTECT,
        verbose_name=_('Position')
    )
    level = models.CharField(max_length=6, verbose_name=_('Level'), null=True, blank=True)
    modality = models.CharField(
        max_length=7,
        choices=[('monthly', _('Monthly')), ('hourly', _('Hourly'))],
        verbose_name=_('Modality')
    )
    base_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Base Salary')
    )

    def __str__(self):
        money = _('$')
        return f'{self.display_position()} - {money}{self.base_salary}'

    def display_salary(self):
        money = _('$')
        return f'{money} {self.base_salary} - ({self.get_modality_display()})'

    def display_position(self):
        level = self.level if self.level else ''

        return f'{self.position} {level}'

    class Meta:
        verbose_name = _('Salary')
        constraints = [
            models.UniqueConstraint(fields=['position', 'level'], name='unique_position_level')
        ]


class SalaryAdjustment(models.Model):
    date = models.DateField(verbose_name=_('Date'))
    salary = models.ForeignKey(
        Salary,
        on_delete=models.PROTECT,
        verbose_name=_('Salary')
    )
    previous_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Previous Salary')
    )
    adjustment_type = models.CharField(
        max_length=10,
        choices=[("percentage", _("Percentage")), ("amount", _("Amount"))],
        verbose_name=_('Adjustment Type')
    )
    adjustment_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Adjustment Value')
    )
    reason = models.TextField(null=True, blank=True, verbose_name=_('Reason'))

    def __str__(self) -> str:
        return f'#{self.pk}'

    def apply_adjustment(self):
        self.previous_salary = self.salary.base_salary

        if self.adjustment_type == "percentage":
            adjustment_amount = self.salary.base_salary * (self.adjustment_value / 100)
            new_salary = self.salary.base_salary + adjustment_amount
            self.salary.base_salary = new_salary

        elif self.adjustment_type == "amount":
            new_salary = self.salary.base_salary + self.adjustment_value
            self.salary.base_salary = new_salary

        self.salary.save()


    def save(self, *args, **kwargs) -> None:
        self.apply_adjustment()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Salary Adjustment')
        constraints = [
            models.UniqueConstraint(fields=['date', 'salary'], name='unique_date_salary')
        ]


class Employee(models.Model):
    first_name = models.CharField(max_length=50, verbose_name=_('First name'))
    last_name = models.CharField(max_length=80, verbose_name=_('Last name'))
    pis_number = models.CharField(max_length=11, verbose_name=_('Pis number'), unique=True)
    position = models.ForeignKey(
        EmployeePosition,
        on_delete=models.PROTECT,
        verbose_name=_('Position')
    )

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = _('Employee')

class EmployeeHiring(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        verbose_name=_('Employee')
    )
    admission_date = models.DateField(blank=True, verbose_name=_('Admission date'))
    expiry_of_experience = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Expiry of experience')
    )
    termination_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Termination date')
    )
    enterprise =  models.ForeignKey(
        'core.Enterprise',
        on_delete=models.PROTECT,
        verbose_name=_('Enterprise')
    )
    vacation_expiration_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Vacation Expiration Date')
    )
    grant_limit = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Grant Limit')
    )
    salary = models.ForeignKey(
        Salary,
        on_delete=models.PROTECT,
        verbose_name=_('Position')
    )

    def save(self, *args, **kwargs) -> None:
        if self.pk is None:

            if EmployeeHiring.objects.filter(
                employee=self.employee,
                termination_date__isnull=True,
                enterprise=self.enterprise
            ).exists():

                raise ActiveEmployeeHiring(_('There is already a hiring with this employee!'))

        return super().save(*args, **kwargs)

    def time_limit_for_vacation(self):
        if self.termination_date:
            return ''

        qty_vacation_taken = len(Vacation.objects.filter(employee_hiring=self))

        acquisition_period_end = self.admission_date + \
            datetime.timedelta(days=365 * (qty_vacation_taken + 1))
        vacation_limit = (
            acquisition_period_end + datetime.timedelta(days=333)
            )

        return vacation_limit

    def get_paid_off(self):
        last = Vacation.objects.filter(
                employee_hiring=self).order_by('-start_date').first()
        return last.paid_off if last else ''

    @property
    def status(self):
        return _('Active') if not self.termination_date else _('Inactive')

    def __str__(self) -> str:
        return f'{self.employee}'

    class Meta:
        verbose_name = _('Employee Hiring')
        verbose_name_plural = _('Employee Hirings')


class Holiday(models.Model):
    day = models.IntegerField(verbose_name=_('Day'))
    month = models.IntegerField(verbose_name=_('Month'))
    description = models.CharField(max_length=100, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Holiday')


class Point(models.Model):
    employee_hiring = models.ForeignKey(EmployeeHiring, on_delete=models.PROTECT)
    date = models.DateField()
    first_entry = models.TimeField(default=datetime.time(0), blank=True)
    first_exit = models.TimeField(default=datetime.time(0), blank=True)
    second_entry = models.TimeField(default=datetime.time(0), blank=True)
    second_exit = models.TimeField(default=datetime.time(0), blank=True)
    third_entry = models.TimeField(default=datetime.time(0), blank=True)
    third_exit = models.TimeField(default=datetime.time(0), blank=True)

    @property
    def total_hours(self):
        x = datetime.datetime.combine(self.date, self.first_exit) - \
            datetime.datetime.combine(self.date, self.first_entry)
        y = datetime.datetime.combine(self.date, self.second_exit) - \
            datetime.datetime.combine(self.date, self.second_entry)
        z = datetime.datetime.combine(self.date, self.third_exit) - \
            datetime.datetime.combine(self.date, self.third_entry)
        return x + y + z

    @classmethod
    def is_there_time_sheet(cls, employee_hiring, date):
        exists = Point.objects.filter(
            employee_hiring=employee_hiring,
            date=date
        ).exists()
        return exists

    @classmethod
    def create_time_sheet(cls, employee_hiring, month, year):
        calendar = TextCalendar(0).formatmonth(year, month).split()
        number_of_day = int(calendar[-1])
        day = 1

        while day <= number_of_day:
            date =  datetime.date(year, month, day)

            if not cls.is_there_time_sheet(employee_hiring, date):
                point = Point.objects.create(
                    employee_hiring=employee_hiring,
                    date=date
                )
                point.save()

            day += 1

    def this_point_existis(self, point):
        point_list = [
            self.first_entry,
            self.first_exit,
            self.second_entry,
            self.second_exit,
            self.third_entry,
            self.third_exit
        ]

        return point in point_list

    
    def calculate_night_shift_bonus(self):
        """Calculates the total night shift bonus time in hours."""
        night_period_start = datetime.time(21, 59)
        night_period_end = datetime.time(5, 0)

        def calculate_night_time(entry, exit):
            if entry == exit:  # If entry and exit are the same, no work was done.
                return datetime.timedelta()

            if entry < exit:  # Normal period within the same day
                return self._time_within_night_period(entry, exit, night_period_start, night_period_end)
            else:  # Period crossing midnight
                return (
                    self._time_within_night_period(entry, datetime.time(23, 59, 59), night_period_start, night_period_end) +
                    self._time_within_night_period(datetime.time(0, 0), exit, night_period_start, night_period_end)
                )

        total_night_time = (
            calculate_night_time(self.first_entry, self.first_exit) +
            calculate_night_time(self.second_entry, self.second_exit) +
            calculate_night_time(self.third_entry, self.third_exit)
        )

        return total_night_time

    @staticmethod
    def _time_within_night_period(entry, exit, night_start, night_end):
        """Calculates the time worked within the night period."""
        if entry >= exit:
            return datetime.timedelta()

        if night_end < night_start:  # Night period crossing midnight (22h-05h)
            if entry >= night_start or exit <= night_end:  
                # Completely within the night period
                return datetime.timedelta(hours=exit.hour - entry.hour, minutes=exit.minute - entry.minute, seconds=exit.second - entry.second)

            if entry < night_start and exit > night_start:  
                # Entry before 22:00 and exit after 22:00
                return datetime.timedelta(hours=exit.hour - night_start.hour, minutes=exit.minute - night_start.minute, seconds=exit.second - night_start.second)

            if entry < night_end and exit > night_end:
                # Entry before 05:00 and exit after 05:00
                return datetime.timedelta(hours=night_end.hour - entry.hour, minutes=night_end.minute - entry.minute, seconds=night_end.second - entry.second)

        else:  # Case where the night period is within the same day (e.g., 22h-23h)
            entry = max(entry, night_start)
            exit = min(exit, night_end)

            if entry >= exit:
                return datetime.timedelta()

            return datetime.timedelta(hours=exit.hour - entry.hour, minutes=exit.minute - entry.minute, seconds=exit.second - entry.second)

        return datetime.timedelta()

    class Meta:
        verbose_name = _('Point')


class Observation(models.Model):
    point = models.ForeignKey(Point, on_delete=models.PROTECT, verbose_name=_('Point'))
    description = models.TextField(verbose_name=_('Descrição'))

    class Meta:
        verbose_name = _('Observation')


class Vacation(models.Model):
    employee_hiring = models.ForeignKey(
        EmployeeHiring,
        on_delete=models.PROTECT,
        verbose_name=_('Employee Hiring')
    )
    start_date = models.DateField(verbose_name=_('Start date'))
    end_date = models.DateField(verbose_name=_('End date'))
    paid_off = models.IntegerField(default=0)

    def is_it_less_than_fourteen_days(self):
        vacation_duration = (self.end_date - self.start_date).days

        return vacation_duration < 14

    def was_it_thirty_days(self):
        vacation_duration = self.vacation_duration()

        return vacation_duration == 30

    def vacation_duration(self):
        return (self.end_date - self.start_date).days + 1

    def is_within_the_limit(self):
        try:
            return self.start_date <= self.employee_hiring.grant_limit
        except TypeError as exc:
            raise NoLimitConcession(_('There is no registered limit concession.')) from exc

    def save(self, *args, **kwargs) -> None:
        self.paid_off = 0
        if self.was_it_thirty_days() and self.is_within_the_limit():
            self.paid_off = 30
        elif self.is_within_the_limit():
            last = Vacation.objects.filter(
                employee_hiring=self.employee_hiring).order_by('-start_date').first()
            if last and last.paid_off < 30:
                self.paid_off = self.vacation_duration() + last.paid_off
            else:
                self.paid_off = self.vacation_duration()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        taken_from = _('Taken from')
        to = _('to')
        return (
            f'{taken_from} {self.start_date.strftime("%d/%m/%Y")} '
            f'{to} {self.end_date.strftime("%d/%m/%Y")}'
        )

    class Meta:
        verbose_name = _('Vacation')
        constraints = [
            models.UniqueConstraint(
                fields=['employee_hiring', 'start_date', 'end_date'],
                name='unique_employee_hiring_start_and_end_date'
            ),
        ]


class HoursBank(models.Model):
    employee_hiring = models.ForeignKey(
        EmployeeHiring,
        on_delete=models.PROTECT,
        verbose_name=_('Employee Hiring')
    )
    date = models.DateField(verbose_name=_('Date'))
    hours_owed = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Hours owed')
    )
    hours_compensated = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Hours compensated')
    )

    @property
    def balance(self):
        return self.hours_owed - self.hours_compensated

    class Meta:
        verbose_name = _('Hours Bank')


def rename_file(_, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('flowerp/documents/', new_filename)

class Document(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    employee_hiring = models.ForeignKey(
        EmployeeHiring,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_('Employee Hiring')
    )
    issue_date = models.DateField(verbose_name=_('Issue date'), null=True, blank=True)
    expiration_date = models.DateField(verbose_name=_('Expiration date'), null=True, blank=True)
    file = models.FileField(upload_to=rename_file, verbose_name=_('File'))

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = _('Document')
