from datetime import date, timedelta


def format_date(date_object):
    # Structures dates in "month day year" form for plot title.
    return date_object.strftime("%B %d %Y")


def today_date():
    today = date.today()
    return format_date(today)


def week_ago_date():
    today = date.today()
    return format_date(today - timedelta(days=6))


def today_date_numeric():
    today = date.today()
    return today.strftime("%d%m%y")
