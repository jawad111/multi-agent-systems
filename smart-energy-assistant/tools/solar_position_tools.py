from datetime import datetime, time, date, timedelta
from math import sin, cos, radians
from astral import LocationInfo
from astral.sun import sun
import pytz

class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vector3(x={self.x}, y={self.y}, z={self.z})"

class SunPositionModel:
    def __init__(self, azimuth: float, elevation: float):
        self.azimuth = azimuth
        self.elevation = elevation

    def __repr__(self):
        return f"SunPositionModel(azimuth={self.azimuth}, elevation={self.elevation})"

class SunTimeModel:
    def __init__(self, sunrise, midday, sunset):
        self.sunrise = sunrise
        self.midday = midday
        self.sunset = sunset

    def __repr__(self):
        return f"SunTimeModel(sunrise={self.sunrise}, midday={self.midday}, sunset={self.sunset})"

class SunPositionHelper:
    def calculate_sun_position(self, latitude: float, longitude: float, current_time: time, current_date: date) -> SunPositionModel:
        # Combine date and time
        dt = datetime.combine(current_date, current_time)
        dt = dt.replace(tzinfo=pytz.timezone("UTC"))  # or local timezone if needed

        # Use astral to get sun data
        location = LocationInfo(latitude=latitude, longitude=longitude)
        sun_data = sun(location.observer, date=dt, tzinfo=pytz.timezone("UTC"))

        # Astral does not return azimuth/elevation directly at arbitrary times, you'd need pyephem or skyfield for that
        # Placeholder fixed values or use external lib if azimuth and altitude at arbitrary time is required
        # For demonstration, returning placeholders
        azimuth = 180.29  # Replace with actual calculation if needed
        elevation = 85.25  # Replace with actual calculation

        print(f"Time: Azimuth - Elevation: {current_time} {azimuth} + {elevation}")
        return SunPositionModel(azimuth, elevation)

    def calculate_relative_position(self, azimuth: float, elevation: float, distance: float) -> Vector3:
        azimuth_rad = radians(azimuth)
        elevation_rad = radians(elevation)

        x = distance * cos(elevation_rad) * sin(azimuth_rad)
        y = distance * sin(elevation_rad)
        z = distance * cos(elevation_rad) * cos(azimuth_rad)

        return Vector3(x, y, z)

    def get_sun_times_based_on_location(self, latitude: float, longitude: float) -> SunTimeModel:
        location = LocationInfo(latitude=latitude, longitude=longitude)
        now = datetime.now().date()
        sun_data = sun(location.observer, date=now, tzinfo=pytz.timezone("UTC"))

        sunrise = sun_data['sunrise']
        midday = sun_data['noon']
        sunset = sun_data['sunset']

        return SunTimeModel(sunrise, midday, sunset)

    def get_current_date_time(self) -> datetime:
        return datetime.now()

    def map_progress_to_time(self, progress: int, sunrise_minutes: int, sunset_minutes: int) -> time:
        total_minutes = sunset_minutes - sunrise_minutes
        current_minutes = sunrise_minutes + (progress * total_minutes // 100)
        return self.minutes_to_time(current_minutes)

    def map_time_to_progress(self, time_string: str, sunrise_minutes: int, sunset_minutes: int) -> int:
        current_minutes = self.time_to_minutes(time_string)
        total_minutes = sunset_minutes - sunrise_minutes
        return max(0, min(100, ((current_minutes - sunrise_minutes) * 100) // total_minutes))

    def minutes_to_time_string(self, total_minutes: int) -> str:
        hours = total_minutes // 60
        minutes = total_minutes % 60
        am_pm_hours = hours - 12 if hours > 12 else hours
        am_pm_suffix = "PM" if hours >= 12 else "AM"
        return f"{am_pm_hours:02}:{minutes:02} {am_pm_suffix}"

    def minutes_to_time(self, total_minutes: int) -> time:
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return time(hour=hours, minute=minutes, second=0)

    def time_to_minutes(self, time_string: str) -> int:
        try:
            parts = time_string.strip().split(":")
            hours = int(parts[0])
            minutes = int(parts[1])
            return hours * 60 + minutes
        except:
            return 0
