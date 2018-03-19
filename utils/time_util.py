
class TimeUtil:
    @staticmethod
    def parse_diff(diff):
        sec = diff.total_seconds()
        mills = diff.microseconds/1000

        minutes, seconds = divmod(sec, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        return int(days), int(hours), int(minutes), int(seconds), int(mills)
