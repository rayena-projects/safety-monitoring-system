"""
Entry point for the Personal Safety Monitoring System.

This module handles user configuration, setup, and launches the main
monitoring system. It collects baseline heart rate and optional PIN
protection before starting continuous health monitoring.
"""

from health_monitor import HealthMonitor
from ui_utils import UI, Colors


def main():
    """
    Main entry point for the safety monitoring application.

    This function:
    1. Displays welcome message and system overview
    2. Collects user's baseline heart rate configuration
    3. Sets up optional PIN protection for security
    4. Displays configuration summary
    5. Launches the health monitoring system

    User Configuration Flow:
        - Baseline heart rate (40-100 bpm, default: 75)
        - Optional 4-6 digit PIN for safety response authentication
        - PIN confirmation for security

    Raises:
        ValueError: If user enters invalid heart rate (outside 40-100 range)
        KeyboardInterrupt: If user cancels setup with CTRL+C

    Example:
        $ python3 main.py
        Welcome! Enter your usual resting heart rate: 72
        Enter a 4-6 digit PIN [or press Enter to skip]: 1234
        Confirm PIN: 1234
        ✓ PIN protection enabled
        [Monitoring begins...]
    """
    UI.header("PERSONAL SAFETY MONITORING SYSTEM", Colors.BRIGHT_MAGENTA)

    print(f"{Colors.CYAN}Welcome! This system monitors your vital signs to detect")
    print(f"potential safety issues and can alert your emergency contacts.{Colors.RESET}")
    print()

    # Collect baseline heart rate
    UI.subheader("⚙️  CONFIGURATION SETUP", Colors.BRIGHT_BLUE)

    while True:
        try:
            baseline_hr = input(f"{Colors.BOLD}Enter your usual resting heart rate (bpm) {Colors.YELLOW}[default: 75]{Colors.RESET}: ").strip()
            if baseline_hr == "":
                baseline_hr = 75
                break
            else:
                baseline_hr = int(baseline_hr)
                if 40 <= baseline_hr <= 100:
                    break
                else:
                    UI.warning("Please enter a realistic heart rate between 40-100 bpm")
        except ValueError:
            UI.error("Please enter a valid number")

    UI.success(f"Baseline heart rate set to: {baseline_hr} bpm")

    # Collect safety PIN
    print()
    UI.subheader("🔐 SAFETY PIN SETUP (Optional but Recommended)", Colors.YELLOW)

    print(f"{Colors.CYAN}A PIN prevents others from responding 'YES' or removing the watch")
    print(f"without your knowledge, providing an extra layer of security.{Colors.RESET}\n")

    safety_pin = input(f"{Colors.BOLD}Enter a 4-6 digit PIN {Colors.YELLOW}[or press Enter to skip]{Colors.RESET}: ").strip()

    if safety_pin:
        if len(safety_pin) < 4 or len(safety_pin) > 6:
            UI.warning("PIN should be 4-6 digits. Using no PIN for this session.")
            safety_pin = ""
        else:
            # Confirm PIN
            confirm_pin = input(f"{Colors.BOLD}Confirm PIN:{Colors.RESET} ").strip()
            if confirm_pin != safety_pin:
                UI.warning("PINs don't match. Using no PIN for this session.")
                safety_pin = ""
            else:
                UI.success(f"PIN protection enabled: {Colors.BOLD}{safety_pin}{Colors.RESET}")
    else:
        UI.info("No PIN protection (responses won't require PIN)", "🔓")

    # Show configuration summary
    config_items = [
        f"{Colors.GREEN}Baseline Heart Rate:{Colors.RESET} {baseline_hr} bpm",
        f"{Colors.GREEN}PIN Protection:{Colors.RESET} {'Enabled (' + safety_pin + ')' if safety_pin else 'Disabled'}",
    ]
    UI.status_box("CONFIGURATION SUMMARY", config_items)

    print(f"{Colors.CYAN}NOTE: In a real smartwatch app, you would also configure:")
    print(f"  • Emergency contact names and phone numbers")
    print(f"  • Preferred notification methods")
    print(f"  • Sensitivity settings{Colors.RESET}\n")

    # Start monitoring
    monitor = HealthMonitor(baseline_heart_rate=baseline_hr, safety_pin=safety_pin)
    monitor.start_monitoring()


if __name__ == "__main__":
    main()
