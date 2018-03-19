from utils.time_util import TimeUtil
import datetime
import unittest

class TestTime(unittest.TestCase):

    def test_time(self):
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(
            milliseconds=(86400 + 7200 + 1380 + 14 + .075) * 1000) #2 дня 2 часа 23 минуты 14 секунд 75 миллисекунд

        diff = end_time - start_time

        days, hours, minutes, seconds, mills = TimeUtil.parse_diff(diff)
        print("{0}д, {1}ч, {2}м, {3}с, {4}мс "
              .format(days, hours, minutes, seconds, mills))

if __name__ == '__main__':
    unittest.main()
