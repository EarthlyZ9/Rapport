import datetime


class ScheduleService:
    @staticmethod
    def time_format_validator(time: datetime.time):
        time_format = "%H:%M"
        try:
            datetime.datetime.strptime(str(time), time_format)
            datetime.time(time.hour, time.minute)
            return True
        except ValueError:
            return False

    @staticmethod
    def date_format_validator(date: datetime.date):
        date_format = "%Y-%m-%d"
        try:
            datetime.datetime.strptime(str(date), date_format)
            print(date, type(date))
            datetime.datetime(date.year, date.month, date.day)
            return True
        except ValueError:
            return False
