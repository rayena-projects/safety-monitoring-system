"""
Simulates sensor data for testing the safety monitoring system.

This module generates realistic sensor readings to simulate various scenarios
including drink spiking incidents. In production, this would be replaced with
actual sensor data from smartwatch hardware (heart rate monitor, accelerometer).
"""

import random
from sensor_reading import SensorReading


class SensorSimulator:
    """
    Generates simulated sensor readings for testing and demonstration.

    This simulator creates realistic heart rate and motion patterns that mimic
    potential drink spiking scenarios. The weighted distribution ensures that
    abnormal patterns occur frequently enough to demonstrate the system's
    detection capabilities.

    Design Rationale:
        - 60% no motion: Realistic for sitting at bar/table during social event
        - Weighted HR distribution: Mix of normal and abnormal to trigger alerts
        - Abnormal ranges: Tachycardia (high HR) and bradycardia (low HR) are
          common physiological responses to drink spiking substances

    Note:
        In production, this entire class would be replaced with:
        - Apple Watch HealthKit integration
        - Fitbit Web API
        - Generic Bluetooth LE heart rate monitor
        - Smartwatch accelerometer data
    """

    @staticmethod
    def generate_reading() -> SensorReading:
        """
        Generate a single simulated sensor reading.

        Creates a realistic sensor data point with weighted probabilities
        designed to simulate drink spiking scenarios:

        Motion Distribution:
            - 60% no motion (stationary/sitting)
            - 40% motion detected

        Heart Rate Distribution:
            - 40% normal range (50-80 bpm)
            - 30% tachycardia (80-130 bpm) - elevated heart rate
            - 30% bradycardia (40-50 bpm) - depressed heart rate

        Returns:
            SensorReading: A new sensor reading with simulated heart rate
                          and motion detection status

        Example:
            >>> reading = SensorSimulator.generate_reading()
            >>> print(f"HR: {reading.heart_rate}, Motion: {reading.motion_detected}")
            HR: 95, Motion: False
        """
        # 60% chance of no motion (realistic for sitting at bar/table)
        # Abnormality detection only triggers when stationary + abnormal HR
        motion = random.random() > 0.6

        # Generate heart rate with weighted distribution
        # 40% normal range (50-80 bpm), 60% potentially abnormal
        if random.random() < 0.4:
            # Normal resting heart rate range
            heart_rate = random.randint(50, 80)
        else:
            # Potentially abnormal - either low or high
            if random.random() < 0.5:
                # High heart rate - tachycardia
                # Many drink spiking substances cause elevated heart rate
                heart_rate = random.randint(80, 130)
            else:
                # Low heart rate - bradycardia
                # Some sedatives/depressants cause reduced heart rate
                heart_rate = random.randint(40, 50)

        return SensorReading(heart_rate, motion)
