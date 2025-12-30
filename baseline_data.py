"""
Baseline health metrics for personalized anomaly detection.

This module stores the user's normal/baseline physiological measurements
used as a reference point for detecting abnormalities.
"""


class BaselineData:
    """
    Stores baseline health metrics for a user.

    This class maintains the user's typical resting heart rate and other
    baseline measurements. These values are used by the anomaly detection
    algorithm to determine what constitutes "abnormal" for this specific user.

    Attributes:
        _baseline_heart_rate (int): User's typical resting heart rate in bpm

    Note:
        In a production system, this would load from a database or user profile.
        The default of 75 bpm is a typical adult resting heart rate.
    """

    def __init__(self):
        """
        Initialize baseline data with default values.

        In production, this would be populated from user configuration
        or calculated from historical data during onboarding.
        """
        # Default baseline - typical adult resting heart rate
        # In production: load from user profile or database
        self._baseline_heart_rate = 75

    @property
    def baseline_heart_rate(self) -> int:
        """
        Get the user's baseline resting heart rate.

        Returns:
            int: Baseline heart rate in beats per minute (bpm).
                 Typically ranges from 60-100 bpm for healthy adults.
        """
        return self._baseline_heart_rate
