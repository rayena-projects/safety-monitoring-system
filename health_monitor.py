"""
Core health monitoring engine with state machine for safety detection.

This module implements the primary monitoring logic for detecting potential
drink spiking incidents through continuous physiological tracking. It uses
a state machine to manage user responses, consecutive abnormal cycles, and
emergency alert escalation.

Key Components:
    - HealthMonitor: Main monitoring class with state machine
    - TimeoutError: Custom exception for user response timeouts
    - timeout_handler: SIGALRM signal handler for timed prompts

Algorithm Overview:
    1. Collect initial data (cycles 1-4)
    2. Calculate abnormality from sliding window of 5 readings
    3. Abnormality only flagged when: (HR<50 or HR>80) AND no motion
    4. Escalation at 45%+ abnormality with 15-second user response window
    5. Track consecutive abnormal cycles after user confirms safety
    6. Sharp jump detection (>20% increase) triggers immediate check
    7. Final safety check on watch removal

State Machine States:
    - awaiting_user_response: Waiting for delayed response to previous alert
    - user_previously_said_safe: Tracking consecutive abnormals after confirmation
    - consecutive_abnormal_after_yes: Counter for abnormal cycles (0-indexed)
    - alert_sent: Whether emergency alert has been triggered
    - last_abnormality: Previous cycle's score for jump detection
"""

import time
import signal
from typing import List, Optional
from sensor_reading import SensorReading
from sensor_simulator import SensorSimulator
from alert_system import AlertSystem
from ui_utils import UI, Colors


class TimeoutError(Exception):
    """
    Custom exception raised when user fails to respond within timeout period.

    Used in conjunction with SIGALRM signal handling to implement timed
    prompts for safety checks.
    """
    pass


def timeout_handler(signum, frame):
    """
    Signal handler for SIGALRM timeout events.

    Raises TimeoutError when the alarm signal is received, allowing
    the monitoring system to handle non-responses gracefully.

    Args:
        signum: Signal number (SIGALRM)
        frame: Current stack frame (unused)

    Raises:
        TimeoutError: Always raised to break out of input() blocking call
    """
    raise TimeoutError()


class HealthMonitor:
    """
    Main health monitoring system with intelligent anomaly detection.

    This class implements the core monitoring loop and state machine for
    detecting potential safety incidents. It continuously analyzes sensor
    data, prompts users when abnormalities are detected, and escalates to
    emergency contacts when necessary.

    Configuration Constants:
        RESPONSE_TIMEOUT (int): Seconds for user to respond to safety checks (15s)
        CYCLE_DELAY (int): Gap between monitoring cycles (10s)
        ESCALATION_THRESHOLD (int): Abnormality % to trigger user check (45%)
        SHARP_JUMP_THRESHOLD (int): % increase for immediate check (20%)

    Attributes:
        baseline_heart_rate (int): User's configured resting heart rate
        safety_pin (str): Optional PIN for response authentication
        alert_system (AlertSystem): Emergency contact notification system
        last_five_readings (List[SensorReading]): Sliding window for calculation
        awaiting_user_response (bool): Waiting for delayed response flag
        consecutive_abnormal_after_yes (int): Counter for consecutive abnormals
        user_previously_said_safe (bool): User confirmed safety flag
        alert_sent (bool): Emergency alert has been sent flag
        last_abnormality (Optional[float]): Previous cycle's abnormality score

    Example:
        >>> monitor = HealthMonitor(baseline_heart_rate=72, safety_pin="1234")
        >>> monitor.start_monitoring()
        # Begins continuous monitoring with PIN protection
    """
    RESPONSE_TIMEOUT = 15  # seconds - user has 15s to respond
    CYCLE_DELAY = 10  # seconds - 10s gap between cycles
    ESCALATION_THRESHOLD = 45  # 45%+ requires user confirmation
    SHARP_JUMP_THRESHOLD = 20  # >20% jump after yes triggers immediate check

    def __init__(self, baseline_heart_rate: int = 75, safety_pin: str = ""):
        """
        Initialize the health monitoring system.

        Args:
            baseline_heart_rate (int, optional): User's resting heart rate in bpm.
                                                 Defaults to 75 (typical adult rate).
            safety_pin (str, optional): 4-6 digit PIN for response authentication.
                                       Empty string disables PIN protection.

        Example:
            >>> monitor = HealthMonitor(baseline_heart_rate=68, safety_pin="1234")
            >>> monitor = HealthMonitor()  # Uses defaults (75 bpm, no PIN)
        """
        self.baseline_heart_rate = baseline_heart_rate
        self.safety_pin = safety_pin  # PIN required for YES and REMOVE commands
        self.alert_system = AlertSystem()
        self.last_five_readings: List[SensorReading] = []

        # State tracking for intelligent response management
        self.awaiting_user_response = False  # True if we need to ask user again due to no response
        self.consecutive_abnormal_after_yes = 0  # Track consecutive abnormal cycles after user said yes
        self.user_previously_said_safe = False  # Flag to show "user previously said safe"
        self.alert_sent = False  # Track if alert has been sent
        self.last_abnormality: Optional[float] = None  # Track previous abnormality for jump detection

    def start_monitoring(self):
        """
        Start continuous health monitoring until watch is removed.

        This is the main entry point for the monitoring loop. It displays
        system configuration, waits for user to begin, and then enters the
        continuous monitoring loop that only exits when:
        - User types REMOVE command (+ PIN if enabled)
        - User presses CTRL+C
        - Fatal system error occurs

        The monitoring flow:
        1. Display configuration summary and instructions
        2. Wait for user confirmation to begin
        3. Enter monitoring loop (calls _monitoring_loop)
        4. On CTRL+C: perform final safety check
        5. Clean exit

        Raises:
            KeyboardInterrupt: Caught and handled with final safety check
            SystemExit: Propagated from REMOVE command

        Example:
            >>> monitor = HealthMonitor(baseline_heart_rate=70)
            >>> monitor.start_monitoring()
            🛡️  SAFETY MONITORING ACTIVE 🛡️
            [Monitoring continues until watch removed...]
        """
        cycle_count = 1

        UI.header("🛡️  SAFETY MONITORING ACTIVE 🛡️", Colors.BRIGHT_GREEN)

        # Show monitoring info
        info_items = [
            f"{Colors.CYAN}Baseline Heart Rate:{Colors.RESET} {self.baseline_heart_rate} bpm",
            f"{Colors.CYAN}Escalation Threshold:{Colors.RESET} {self.ESCALATION_THRESHOLD}%",
            f"{Colors.CYAN}Sharp Jump Threshold:{Colors.RESET} >{self.SHARP_JUMP_THRESHOLD}%",
        ]

        if self.safety_pin:
            info_items.append(f"{Colors.GREEN}🔐 PIN Protection:{Colors.RESET} ENABLED")
            info_items.append(f"{Colors.YELLOW}Response Format:{Colors.RESET} 'YES {self.safety_pin}' or 'REMOVE {self.safety_pin}'")
        else:
            info_items.append(f"{Colors.YELLOW}🔓 PIN Protection:{Colors.RESET} DISABLED")
            info_items.append(f"{Colors.YELLOW}Response Format:{Colors.RESET} 'YES' or 'REMOVE'")

        UI.status_box("MONITORING SETTINGS", info_items)

        print(f"{Colors.CYAN}📱 To end monitoring:{Colors.RESET}")
        print(f"   • Type {Colors.BOLD}REMOVE{Colors.RESET} (+ PIN if enabled) when prompted")
        print(f"   • Or press {Colors.BOLD}CTRL+C{Colors.RESET} anytime")
        print(f"\n{Colors.GREEN}System will perform a final safety check before ending.{Colors.RESET}\n")

        input(f"{Colors.BOLD}Press Enter to begin monitoring...{Colors.RESET}")

        try:
            self._monitoring_loop(cycle_count)
        except KeyboardInterrupt:
            print(f"\n\n{Colors.BRIGHT_RED}🔴 Watch removal detected (CTRL+C pressed)...{Colors.RESET}")
            self._final_safety_check()

    def _monitoring_loop(self, cycle_count):
        """Main monitoring loop"""
        while True:
            UI.cycle_header(cycle_count)

            # Collect sensor reading
            reading = SensorSimulator.generate_reading()
            self.last_five_readings.append(reading)
            if len(self.last_five_readings) > 5:
                self.last_five_readings.pop(0)

            # First 4 cycles: only collecting data, abnormality is always 0
            if cycle_count <= 4:
                print(f"{Colors.YELLOW}📊 Collecting initial data... ({cycle_count}/4){Colors.RESET}")
                UI.progress_bar(cycle_count, 4)
                print(f"\n{Colors.CYAN}Heart Rate:{Colors.RESET} {Colors.BOLD}{reading.heart_rate} bpm{Colors.RESET}")
                print(f"{Colors.CYAN}Motion:{Colors.RESET} {'🏃 Detected' if reading.motion_detected else '🧍 Not Detected'}")
                print(f"{Colors.GREEN}Abnormality: 0%{Colors.RESET}")
            else:
                # Calculate abnormality percentage (from cycle 5 onwards using current + previous 4)
                abnormality = self._calculate_abnormality(self.last_five_readings)

                print(f"{Colors.CYAN}Heart Rate:{Colors.RESET} {Colors.BOLD}{reading.heart_rate} bpm{Colors.RESET}")
                print(f"{Colors.CYAN}Motion:{Colors.RESET} {'🏃 Detected' if reading.motion_detected else '🧍 Not Detected'}")

                # Show abnormality gauge
                UI.abnormality_gauge(abnormality)

                # Check if we need to ask user again due to previous no response
                if self.awaiting_user_response:
                    print("\n⚠️  Previous cycle had no response - checking again...")
                    safe = self._prompt_user_safety()

                    if safe:
                        print("✓ User confirmed safety.")
                        if self.alert_sent:
                            print("📢 Previously an alert was sent to your contacts.")
                            print("   Please inform them that you are safe.")
                        # Reset state and return to normal flow
                        self.awaiting_user_response = False
                        self.alert_sent = False
                        self.consecutive_abnormal_after_yes = 0
                        self.user_previously_said_safe = False
                    else:
                        # No response again - send alert again
                        print("⚠️  No response again - sending alert to emergency contacts!")
                        self.alert_system.send_alert()
                        self.alert_sent = True
                        # Reset and go back to normal flow
                        self.awaiting_user_response = False
                        self.consecutive_abnormal_after_yes = 0
                        self.user_previously_said_safe = False

                # Normal flow - check abnormality level
                elif abnormality > self.ESCALATION_THRESHOLD:
                    # Abnormality > 45%

                    # Check if user previously said safe and we're tracking consecutive abnormal
                    if self.user_previously_said_safe:
                        print("📝 Note: User previously responded safe")

                        # Check for sharp jump >20% from previous abnormality
                        sharp_jump_detected = False
                        if self.last_abnormality is not None:
                            jump = abnormality - self.last_abnormality
                            if jump > self.SHARP_JUMP_THRESHOLD:
                                sharp_jump_detected = True
                                print(f"⚠️  SHARP JUMP DETECTED: {round(jump)}% increase from previous cycle!")
                                print("Checking on user immediately...")

                        # Increment AFTER checking for sharp jump
                        self.consecutive_abnormal_after_yes += 1

                        # Display count for debugging
                        print(f"   (Consecutive abnormal cycles after 'yes': {self.consecutive_abnormal_after_yes})")

                        # Ask on sharp jump OR after exactly 3 consecutive abnormal cycles
                        if sharp_jump_detected or self.consecutive_abnormal_after_yes >= 3:
                            if self.consecutive_abnormal_after_yes >= 3 and not sharp_jump_detected:
                                print("⚠️  3rd consecutive abnormal cycle after 'yes' - checking on user...")

                            safe = self._prompt_user_safety()

                            if safe:
                                print("✓ User confirmed safety.")
                                # Reset tracking and start fresh
                                self.consecutive_abnormal_after_yes = 0
                                self.user_previously_said_safe = False
                            else:
                                # No response or no
                                print("⚠️  No response or unsafe - sending alert to emergency contacts!")
                                self.alert_system.send_alert()
                                self.awaiting_user_response = True
                                self.alert_sent = True
                                self.consecutive_abnormal_after_yes = 0
                                self.user_previously_said_safe = False
                        # else: just note it and continue (1st or 2nd consecutive, no sharp jump)
                    else:
                        # First time seeing >45% or not tracking consecutive
                        safe = self._prompt_user_safety()

                        if safe:
                            print("✓ User confirmed safety.")
                            # Start tracking consecutive abnormal cycles
                            # Set counter to 0 - we'll increment on NEXT abnormal cycle
                            self.user_previously_said_safe = True
                            self.consecutive_abnormal_after_yes = 0
                        else:
                            # No response or no
                            print("⚠️  No response or unsafe - sending alert to emergency contacts!")
                            self.alert_system.send_alert()
                            self.awaiting_user_response = True
                            self.alert_sent = True
                            self.user_previously_said_safe = False

                else:
                    # Abnormality 0-45% (normal)
                    if self.user_previously_said_safe:
                        # Check if this breaks the consecutive abnormal pattern
                        # If we had consecutive abnormal and now it's normal, reset
                        print("Status: Normal")
                        # Reset the consecutive counter but we might continue tracking
                        # Based on spec: "if consecutive cycles are normal or alternately normal and abnormal"
                        # We reset completely when we get normal readings
                        self.consecutive_abnormal_after_yes = 0
                        self.user_previously_said_safe = False
                    else:
                        print("Status: Normal - No escalation needed")

                # Store current abnormality for next cycle's jump detection
                self.last_abnormality = abnormality

            cycle_count += 1

            # Delay between cycles (10 seconds) with ability to skip or remove
            print(f"\nNext cycle in {self.CYCLE_DELAY} seconds...")
            if self.safety_pin:
                print("(Press Enter to continue immediately)")
            else:
                print("(Press Enter to continue, or type REMOVE to end)")

            # Non-blocking wait with timeout
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(self.CYCLE_DELAY)

            try:
                user_input = input().strip()
                signal.alarm(0)  # Cancel alarm

                # Parse input for REMOVE command with optional PIN
                if user_input:
                    parts = user_input.split()
                    command = parts[0].upper()

                    if command == "REMOVE":
                        # Check PIN if required
                        if self.safety_pin:
                            if len(parts) < 2 or parts[1] != self.safety_pin:
                                print("⚠️  Incorrect or missing PIN - continuing monitoring")
                            else:
                                print("\n🔴 Watch removal detected...")
                                self._final_safety_check()
                                return  # Exit monitoring loop
                        else:
                            print("\n🔴 Watch removal detected...")
                            self._final_safety_check()
                            return  # Exit monitoring loop
                # If just Enter or anything else, continue to next cycle
            except TimeoutError:
                signal.alarm(0)  # Timeout - continue to next cycle
                pass
            except Exception:
                signal.alarm(0)
                pass

    def _calculate_abnormality(self, window: List[SensorReading]) -> float:
        """
        Calculate abnormality score from a sliding window of sensor readings.

        This is the core detection algorithm. Abnormality is ONLY flagged when:
        - Heart rate < 50 bpm (bradycardia) OR > 80 bpm (tachycardia)
        - AND there is NO movement detected (user is stationary)

        The combination of abnormal HR + no motion is critical for detecting
        drink spiking while avoiding false positives from exercise or stress.

        Scoring Algorithm:
            - HR > 110 bpm (no motion): +25 points
            - HR 100-110 bpm (no motion): +20 points
            - HR 90-100 bpm (no motion): +15 points
            - HR 80-90 bpm (no motion): +10 points
            - HR < 45 bpm (no motion): +20 points
            - HR 45-50 bpm (no motion): +10 points
            - Maximum score: 100 (capped)

        Args:
            window (List[SensorReading]): Sliding window of 5 recent readings

        Returns:
            float: Abnormality score from 0-100
                  0-45: Normal, no action
                  45+: Escalation threshold, prompts user

        Example:
            >>> readings = [SensorReading(110, False) for _ in range(5)]
            >>> abnormality = monitor._calculate_abnormality(readings)
            >>> print(abnormality)  # 100 (5 readings × 25 points, capped at 100)
        """
        score = 0
        for r in window:
            hr = r.heart_rate
            # Only count as abnormal if: (HR < 50 OR HR > 80) AND no motion
            if not r.motion_detected and (hr < 50 or hr > 80):
                # Higher deviation = higher score
                if hr > 110:
                    score += 25
                elif hr > 100:
                    score += 20
                elif hr > 90:
                    score += 15
                elif hr > 80:
                    score += 10
                elif hr < 45:
                    score += 20
                elif hr < 50:
                    score += 10
        return min(100, score)

    def _prompt_user_safety(self) -> bool:
        """
        Prompt user for safety confirmation with timeout and PIN validation.

        Displays a safety check prompt with RESPONSE_TIMEOUT (15 seconds)
        for the user to respond. If PIN protection is enabled, validates
        the provided PIN before accepting the response.

        User can respond with:
        - "YES [PIN]" (if PIN enabled) or "YES" (no PIN): Confirms safety
        - "REMOVE [PIN]" or "REMOVE": Ends monitoring session
        - No response: Timeout after 15 seconds, treated as unsafe

        Timeout Implementation:
            Uses UNIX SIGALRM signal for non-blocking input with timeout.
            On Windows, this may not work (SIGALRM not available).

        Args:
            None (uses instance variables for PIN and timeout settings)

        Returns:
            bool: True if user confirmed safety ("YES" with correct PIN)
                 False if no response, incorrect PIN, or any other input

        Raises:
            SystemExit: If user types REMOVE command (exits monitoring)

        Example:
            With PIN:
                User types: "YES 1234"
                Returns: True (if 1234 is correct PIN)

            Without PIN:
                User types: "YES"
                Returns: True

            Timeout:
                User doesn't respond within 15s
                Returns: False (triggers alert)
        """
        if self.safety_pin:
            print(f"\n🔔 Are you okay? Type 'YES [PIN]' within {self.RESPONSE_TIMEOUT} seconds:")
            print(f"   (or type 'REMOVE [PIN]' to end monitoring)")
        else:
            print(f"\n🔔 Are you okay? Type YES within {self.RESPONSE_TIMEOUT} seconds:")

        # Set up signal handler for timeout
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(self.RESPONSE_TIMEOUT)

        try:
            response = input().strip()
            signal.alarm(0)  # Cancel the alarm

            # Parse response (could be "YES PIN" or "REMOVE PIN" or just "YES"/"REMOVE")
            parts = response.split()
            if not parts:
                return False

            command = parts[0].upper()

            # Check if PIN is required and validate it
            if self.safety_pin:
                if len(parts) < 2:
                    print("⚠️  PIN required but not provided")
                    return False
                provided_pin = parts[1]
                if provided_pin != self.safety_pin:
                    print("⚠️  Incorrect PIN")
                    return False

            # Check for REMOVE command
            if command == "REMOVE":
                print("\n🔴 Watch removal detected...")
                self._final_safety_check()
                raise SystemExit()  # Exit the program

            return command == "YES"
        except TimeoutError:
            signal.alarm(0)  # Cancel the alarm
            print("\n⏱️  Time expired - no response received")
            return False
        except SystemExit:
            raise  # Re-raise to exit
        except Exception:
            signal.alarm(0)  # Cancel the alarm
            return False

    def _final_safety_check(self):
        """Always ask user if they're safe before terminating, regardless of abnormality"""
        print("\n" + "="*60)
        print("FINAL SAFETY CHECK BEFORE ENDING SESSION")
        print("="*60)
        print(f"Are you safe? Type YES within {self.RESPONSE_TIMEOUT} seconds:")

        # Set up signal handler for timeout
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(self.RESPONSE_TIMEOUT)

        try:
            response = input()
            signal.alarm(0)  # Cancel the alarm
            if response.strip().upper() == "YES":
                print("\n✓ User confirmed safety.")
                print("Monitoring session ended. Stay safe!")
            else:
                print("\n⚠️  Unsafe response - sending alert to emergency contacts!")
                self.alert_system.send_alert()
                print("Monitoring session ended.")
        except TimeoutError:
            signal.alarm(0)  # Cancel the alarm
            print("\n⚠️  No response - sending alert to emergency contacts!")
            self.alert_system.send_alert()
            print("Monitoring session ended.")
        except Exception:
            signal.alarm(0)  # Cancel the alarm
            print("\n⚠️  Error - sending alert to emergency contacts as precaution!")
            self.alert_system.send_alert()
            print("Monitoring session ended.")
