"""
Data model for sensor readings from wearable health monitoring device.

This module defines the SensorReading class which encapsulates heart rate
and motion sensor data from a smartwatch or fitness tracker.
"""


class SensorReading:
    """
    Immutable data class representing a single sensor reading snapshot.

    This class holds physiological and motion data captured at a specific
    moment in time. Used throughout the monitoring system to track the
    user's health status.

    Attributes:
        _heart_rate (int): Heart rate in beats per minute (bpm)
        _motion_detected (bool): Whether motion was detected by accelerometer

    Example:
        >>> reading = SensorReading(heart_rate=72, motion_detected=True)
        >>> print(f"HR: {reading.heart_rate} bpm, Motion: {reading.motion_detected}")
        HR: 72 bpm, Motion: True
    """

    def __init__(self, heart_rate: int, motion_detected: bool):
        """
        Initialize a new sensor reading.

        Args:
            heart_rate (int): Heart rate measurement in beats per minute (bpm).
                             Typically ranges from 40-200 bpm for humans.
            motion_detected (bool): True if motion was detected by accelerometer,
                                   False if user appears stationary.
        """
        self._heart_rate = heart_rate
        self._motion_detected = motion_detected

    @property
    def heart_rate(self) -> int:
        """
        Get the heart rate measurement.

        Returns:
            int: Heart rate in beats per minute (bpm)
        """
        return self._heart_rate

    @property
    def motion_detected(self) -> bool:
        """
        Get the motion detection status.

        Returns:
            bool: True if motion was detected, False if stationary
        """
        return self._motion_detected
