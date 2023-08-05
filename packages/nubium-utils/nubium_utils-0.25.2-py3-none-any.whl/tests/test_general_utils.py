from datetime import datetime
from unittest import TestCase

from pytz import timezone

from nubium_utils.general_utils import universal_datetime_converter


class TestGeneralUtils(TestCase):
    def test_universal_datetime_converter(self):
        eastern_timezone = timezone("America/New_York")
        expected_output = "2021-05-27T10:15:00Z"

        # "TEST CASE: " string will be printed for any input that fails, to help you debug which one is failing
        inputs = [("2021-05-27 06:15:00", eastern_timezone, expected_output, "TEST CASE: string in Eastern"),
                  ("2021-05-27 10:15:00", None, expected_output, "TEST CASE: string in UTC"),
                  (datetime(2021, 5, 27, 6, 15), eastern_timezone, expected_output, "TEST CASE: datetime in Eastern"),
                  (datetime(2021, 5, 27, 10, 15), None, expected_output, "TEST CASE: datetime in UTC"),
                  ("2021-05-27", None, "2021-05-27T00:00:00Z", "TEST CASE: date only, no time"),
                  ("I am not a date", None, "", "TEST CASE: junk data"),
                  ("2021-05-27T10:15:00Z", None, expected_output, "TEST CASE: already in universal format"),
                  ("2021-05-27T06:15:00-04:00", None, expected_output, "TEST CASE: with +/- offset")]

        for input_datetime in inputs:
            args = [input_datetime[0]] if input_datetime[1] is None else [input_datetime[0], input_datetime[1]]
            self.assertEqual(universal_datetime_converter(*args), input_datetime[2], input_datetime[3])
