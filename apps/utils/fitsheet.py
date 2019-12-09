import locale
from decimal import Decimal
from django.utils.encoding import smart_text
from . import arial10


class FitSheetWrapper(object):
    """Try to fit columns to max size of any entry.
    To use, wrap this around a worksheet returned from the
    workbook's add_sheet method, like follows:
        sheet = FitSheetWrapper(book.add_sheet(sheet_name))
    The worksheet interface remains the same: this is a drop-in wrapper
    for auto-sizing columns.
    """

    def __init__(self, sheet):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        self.sheet = sheet
        self.widths = dict()

    def write(self, r, c, label='', *args, **kwargs):
        self.sheet.write(r, c, label, *args, **kwargs)
        if type(label) == Decimal:
            label = locale.currency(label, grouping=True)
        else:
            try:
                label = str(label)
            except Exception:
                label = smart_text(label)
                label = label.encode('ascii', 'replace')
        width = int(arial10.fitwidth(str(label)))
        if width > self.widths.get(c, 0):
            self.widths[c] = width
            self.sheet.col(c).width = width

    def __getattr__(self, attr):
        return getattr(self.sheet, attr)