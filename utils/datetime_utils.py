from datetime import datetime, time

def get_datetime_from_time(time_data):
    if isinstance(time_data,datetime):
        time_data = time_data.time()
    elif not isinstance(time_data, time):
        raise TypeError("Expected a datetime.time object for time_data")
    
    return datetime.combine(datetime.today(), time_data)

def get_hour_time_from_second(time_seconds=0):
    return round(time_seconds / 3600, 1)

def get_time_difference(check_in, check_out):
    try:
        check_in_datetime = get_datetime_from_time(check_in)
        check_out_datetime = get_datetime_from_time(check_out)

        time_diff = check_out_datetime - check_in_datetime
        total_seconds = time_diff.total_seconds()
        return get_hour_time_from_second(total_seconds)
    except Exception as e:
        raise ValueError(f"exception is : {e}")

def parse_custom_time_format(time_str):
    try:

        if ':' in time_str:
            hours, minutes = map(int, time_str.split(':'))
            return time(hours, minutes)

        hours, decimal_minutes = map(float, time_str.split('.'))
        minutes = int(decimal_minutes * 6)  
        return time(int(hours), minutes)
        
    except Exception as e:
        raise ValueError(f"Invalid time format '{time_str}': {e}")
        
