from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ToolNotAvailable(ValidationError):
    pass


class ToolCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = _('Tool Category')


class Brand(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = _('Brand')


class ToolStatus(models.TextChoices):
    NEW = ('new', 'New')
    LIGHTLY_USED = ('lightly_used', 'Lightly Used')
    USED = ('used', 'Used')
    WORN = ('worn', 'Worn')
    BROKEN = ('broken', 'Broken')
    UNDER_REPAIR = ('under_repair', 'Under Repair')
    DISCARDED = ('discarded', 'Discarded')


class Tool(models.Model):
    item = models.ForeignKey(
        'product.Product',
        on_delete=models.PROTECT,
        verbose_name=_('Product')
    )

    asset_number = models.CharField(
        max_length=12,
        verbose_name=_('Asset Number')
    )

    serial_number = models.CharField(
        max_length=12,
        verbose_name=_('Serial Number')
    )

    acquisition_date = models.DateField(
        verbose_name=_('Acquisition Date')
    )

    tool_category = models.ForeignKey(
        ToolCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Tool Category')
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Brand')
    )

    tool_status = models.CharField(
        max_length=12,
        choices=ToolStatus.choices,
        verbose_name=_('Tool Status'),
        default=ToolStatus.NEW
    )

    description = models.TextField(
        verbose_name=_('Description')
    )

    class Meta:
        db_table = 'tools'
        verbose_name = _('Tool')
        constraints = [
            models.UniqueConstraint(
                fields=['item', 'asset_number'],
                name='unique_item_asset_number'
            )
        ]

    def __str__(self) -> str:
        return f'{self.item.name} - PAT: {self.asset_number}'


class ToolDistributionRecord(models.Model):
    issue_date = models.DateTimeField(verbose_name=_('Issue date'))

    return_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Return date')
    )

    employee = models.ForeignKey(
        'human_resources.EmployeeHiring',
        on_delete=models.PROTECT
    )

    tool = models.ForeignKey(Tool, on_delete=models.PROTECT)

    def save(self, *args, **kwargs) -> None:
        if ToolDistributionRecord.objects.filter(
            tool=self.tool,
            return_date__isnull=True
        ).exists:
            raise ToolNotAvailable(_('This tool is not available.'))

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        pk = str(self.pk).zfill(3)
        return f'#{pk}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tool', 'employee', 'issue_date'],
                name='unique_tool_employee_date'
            )
        ]


class ToolReturnRecord(models.Model):
    return_date = models.DateTimeField(verbose_name=_('Return date'))

    tool_distribution = models.ForeignKey(
        ToolDistributionRecord,
        on_delete=models.PROTECT
    )
