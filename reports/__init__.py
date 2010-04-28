import datetime

DATE_FORMAT = "%Y-%m-%d"
def date_str_to_python(date_str):
    return datetime.datetime.strptime(date_str, DATE_FORMAT)

OUTPUT_FORMAT = "%A %B %d, %Y" # Monday December 1, 2009
def python_date_to_display_str(python_date):
    return python_date.strftime(OUTPUT_FORMAT).replace(' 0', ' ')

SHORT_OUTPUT_FORMAT = "%B %d" # December 1
def python_date_to_short_display_str(python_date):
    return python_date.strftime(SHORT_OUTPUT_FORMAT).replace(' 0', ' ')

def get_day_of_week_str(python_date):
    return python_date.strftime("%A")
