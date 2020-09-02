import unittest
from sun_angle.main import sun_angle, TimeFormatException


class TestSunAngle(unittest.TestCase):

    def test_valid_results(self):
        input_output = {
            "00:00": "I don't see the sun!",
            "05:00": "I don't see the sun!",
            "06:00": 0,
            "06:01": 0.25,
            "06:10": 2.5,
            "12:15": 93.75,
            "18:00": 180,
            "18:01": "I don't see the sun!",
            "01:23": "I don't see the sun!",
        }

        for input_date, output_data in input_output.items():
            result = sun_angle(input_date)
            self.assertEqual(result, output_data)

    def test_invalid_results(self):
        input_output = (
            "",
            "99:99"
            "00:99",
            "99:00",
            "str",
            "24:60",
            "00;00",
        )

        for input_date in input_output:
            with self.assertRaises(TimeFormatException):
                result = sun_angle(input_date)


if __name__ == '__main__':
    unittest.main()
