from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from human_resources.views import *


app_name = 'human_resources'

urlpatterns = [
    path('', HumanResourcesIndex.as_view(), name='index'),
    path('positions/new/', CreateEmployeePosition.as_view(), name='create_position'),
    path('positions/<int:pk>/', UpdateEmployeePosition.as_view(), name='update_position'),
    path('positions/', ReadEmployeePosition.as_view(), name='read_position'),
    path('employee/new/', CreateEmployee.as_view(), name='create_employee'),
    path('employee/<int:pk>/', UpdateEmployee.as_view(), name='update_employee'),
    path('employee/', ReadEmployee.as_view(), name='read_employee'),
    path('hirings/new/', CreateEmployeeHiring.as_view(), name='create_hiring'),
    path('hirings/<int:pk>/', UpdateEmployeeHiring.as_view(), name='update_hiring'),
    path('vacations/new/', CreateVacation.as_view(), name='create_vacation'),
    path('vacations/expiration/', ReadVacationExpiration.as_view(), name='read_vacation_expiration'),
    path('vacations/<int:pk>/', UpdateVacation.as_view(), name='update_vacation'),
    path('vacations/', ReadVacation.as_view(), name='read_vacation'),
    path('hirings/', ReadEmployeeHiring.as_view(), name='read_hiring'),
    path('points/register/', RegisterPointHenryPrisma.as_view(), name='register_point_henry'),
    path('timesheet/<int:employee_hiring>/<str:month_year>/', TimeSheetEdit.as_view(), name='time_sheet_edit'),
    path('timesheet/pdf/<int:employee_pk>/<str:month_year>/', ReportInPdf.as_view(), name='time_sheet_pdf'),
    path('timesheet/', TimeSheetReport.as_view(), name='time_sheet_report'),
    path('salaries/new/', CreateSalary.as_view(), name='create_salary'),
    path('salaries/<int:pk>/', UpdateSalary.as_view(), name='update_salary'),
    path('salaries/', ReadSalary.as_view(), name='read_salary'),
    path('salaries/adjustments/new', CreateSalaryAdjustment.as_view(), name='create_salary_adjustment'),
    path('salaries/adjustments/<int:pk>/', UpdateSalaryAdjustment.as_view(), name='update_salary_adjustment'),
    path('salaries/adjustments/', ReadSalaryAdjustment.as_view(), name='read_salary_adjustment'),
    path('documents/new', CreateDocument.as_view(), name='create_document'),
    path('documents/', ReadDocument.as_view(), name='read_document'),
    path('documents/<int:document_id>', view_document, name='view_document'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
