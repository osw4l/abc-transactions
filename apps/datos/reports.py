import xlwt, xlrd, re
from datetime import datetime
from django.contrib.humanize.templatetags.humanize import intcomma
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import StreamingHttpResponse
from django.template.defaultfilters import slugify
from .constants import ACTIVE
from apps.utils.fitsheet import FitSheetWrapper
from .models import Transaction


class ReportMain(object):
    query = None
    user = None

    def __init__(self, user=None):
        self.query = Transaction.objects.filter(user=user).order_by('-id')
        self.user = user.get_full_name()

    @property
    def file_name(self):
        return 'transaction_report_{}_{}.xls'.format(
            datetime.now().date(),
            slugify(self.user)
        )


def generate_xls_report(user):
    report = ReportMain(user=user)
    query = report.query
    archivo = report.file_name
    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('transactions_{}'.format(user.get_full_name()))
    row_num = 0
    worksheet = FitSheetWrapper(worksheet)
    columns = ['id', 'user', 'created_at', 'value', 'points', 'status']

    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num])

    for transaction in query:
        row_num += 1
        row = [
            transaction.id,
            transaction.user.get_full_name(),
            transaction.created_at.strftime('%b %d, %Y'),
            intcomma(transaction.value),
            transaction.points,
            'ACTIVE' if transaction.status is ACTIVE else 'INACTIVE'
        ]
        for col_num in range(len(row)):
            worksheet.write(row_num, col_num, row[col_num])

    file = BytesIO()
    workbook.save(file)
    file.seek(0)
    response = StreamingHttpResponse(streaming_content=ContentFile(file.getvalue()),
                                     content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename={}'.format(archivo)
    file.close()
    return response
