import datetime as dt


def get_time_str(start_time, position_in_mins):
    current_time = start_time + dt.timedelta(minutes=position_in_mins)
    return current_time.strftime('%Y-%m-%d %H:%M:%S')


def format_start_time(start_time):
    try:
        return dt.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise RuntimeError("Expect time in YYYY:MM:DD HH:MM:SS format")
