from me_main_libs import *
from pandas.tseries.offsets import BDay


def read_difference_between_dates(start_date, end_date, output_unit='hours'):
    '''
    output_unit: years,days,hours,minutes,seconds,microseconds
    '''
    time_diff = end_date-start_date
    time_diff = time_diff.total_seconds()

    if output_unit == 'years':
        seconds = 31536000
    if output_unit == 'days':
        seconds = 86400
    if output_unit == 'hours':
        seconds = 3600
    if output_unit == 'minutes':
        seconds = 60
    if output_unit == 'seconds':
        return time_diff.seconds
    if output_unit == 'microseconds':
        return time_diff.microseconds

    time_diff = divmod(time_diff, seconds)[0]
    return time_diff


def read_timestamp_to_integer(timestamp, output_unit='seconds'):
    '''
    output_unit: seconds,microseconds
    '''
    timestamp = timestamp.value
    if output_unit == 'seconds':
        return int(timestamp/1000000000)
    if output_unit == 'microseconds':
        return int(timestamp/1000000)


def read_business_days(start_date, end_date):
    dates = pd.date_range(start_date, end_date,
                          freq=BDay())
    return dates
