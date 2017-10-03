from calendar import HTMLCalendar, month_name

from dateutil.relativedelta import relativedelta
from datetime import date

from django.core.urlresolvers import reverse

class Calendar(HTMLCalendar):
    def __init__(self, dates=[]):
        super().__init__()
        self.dates = dates

    def formatmonthname(self, theyear, themonth, withyear=True):
        this_month = date(theyear, themonth, 1)
        prev_month = this_month - relativedelta(months=1)
        next_month = this_month + relativedelta(months=1)

        if withyear:
            this_month_name = '{0} {1}'.format(
                month_name[this_month.month], this_month.year)
            prev_month_name = '{0} {1}'.format(
                month_name[prev_month.month], prev_month.year)
            next_month_name = '{0} {1}'.format(
                month_name[next_month.month], next_month.year)
        else:
            this_month_name = '{0}'.format(month_name[this_month.month])
            prev_month_name = '{0}'.format(month_name[prev_month.month])
            prev_month_name = '{0}'.format(month_name[next_month.month])

        prev_month_link = self.month_link(
            '&laquo;', prev_month.year, prev_month.month, 'float: left'
        )
        next_month_link = self.month_link(
            '&raquo;', next_month.year, next_month.month, 'float: right'
        )

        return '<tr><th colspan="7" class="month">{0}{1}{2}</th></tr>'.format(
            prev_month_link, this_month_name, next_month_link)

    def month_link(self, text, year, month, style):
        link = '<a href="#" onclick="setMonth({0}, {1});" style="{2}">{3}</a>'
        return link.format(year, month, style, text)

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super().formatmonth(year, month)

    def formatday(self, day, weekday):
        if day != 0:
            day_date = date(self.year, self.month, day)
            css_class = self.cssclasses[weekday]
            if date.today() == day_date:
                css_class += ' today'
            if day_date in self.dates:
                css_class += ' highlighted'
            return self.day_cell(css_class, day_date)
        return self.no_day_cell()

    def day_cell(self, css_class, day_date):
        link = '<a href="#" onclick="setDate(\'{0}\');">{1}</a>'.format(
            day_date, day_date.day,
        )
        cell = '<td class="{0}" id="{1}">{2}</td>'.format(
            css_class, day_date, link
        )
        return cell

    def no_day_cell(self):
        return '<td class="noday"><div>&nbsp;</div></td>'
