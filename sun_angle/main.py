import re
from typing import Union


class TimeFormatException(Exception):
    pass


class SunAngle:
    _angle_in_minutes: float = 0.25
    _origin_in_minutes: int = 360
    _minimum_angle: int = 0
    _maximum_angle: int = 180
    _supported_time_format: str = r'^^(([0-1]{1}[0-9]{1})|([2]{1}[0-4]{1})):[0-5]{1}[0-9]{1}$$'

    def __init__(self, current_time: str) -> None:
        self.current_time = current_time

    def calculate_angle(self) -> Union[str, int, float]:
        self.check_time_format(self.current_time)

        time_in_minutes = self.convert_date_to_minutes(self.current_time)
        time_in_minutes_origin = self.bring_time_to_origin(time_in_minutes)
        return self.prepare_angle(time_in_minutes_origin)

    def check_time_format(self, date_time: str) -> None:
        if re.match(self._supported_time_format, date_time):
            return
        else:
            raise TimeFormatException('Unsupported time format %s' % date_time)

    def convert_date_to_minutes(self, date_time: str) -> int:
        hour, minutes = date_time.split(':')
        return self.convert_hours_to_minutes(hour) + int(minutes)

    @staticmethod
    def convert_hours_to_minutes(hour: Union[int, float]) -> int:
        if not isinstance(hour, int):
            hour = int(hour)
        return hour * 60

    def bring_time_to_origin(self, date_time: int) -> int:
        return date_time - self._origin_in_minutes

    def prepare_angle(self, date_time: int) -> Union[str, int, float]:
        row_angle = date_time * self._angle_in_minutes
        if self.should_convert_to_int(row_angle):
            row_angle = int(row_angle)

        if self.check_angle_conditions(row_angle):
            row_angle = "I don't see the sun!"

        return row_angle

    @staticmethod
    def should_convert_to_int(angle: float) -> bool:
        return not angle - int(angle)

    def check_angle_conditions(self, angle: Union[int, float]) -> bool:
        return self._minimum_angle > angle or angle > self._maximum_angle


def sun_angle(input_date: str) -> Union[str, int, float]:
    sun_angle_instance = SunAngle(input_date)
    return sun_angle_instance.calculate_angle()


def run():
    expected_result = {
        "05:00": "I don't see the sun!",
        "06:00": 0,
        "06:01": 0.25,
        "06:10": 2.5,
        "12:15": 93.75,
        "18:00": 180,
        "18:01": "I don't see the sun!",
        "01:23": "I don't see the sun!",
    }

    for input_date, output_data in expected_result.items():
        result = sun_angle(input_date)
        assert result == output_data


if __name__ == "__main__":
    run()
