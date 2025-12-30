"""
UI demonstration script for the Personal Safety Monitoring System.

This standalone demo showcases all the visual enhancements and UI components
without running the actual monitoring system. Useful for previewing the
interface design and testing terminal color support.

Usage:
    python3 demo_ui.py

The demo displays:
    - Header and subheader styles
    - Success/warning/error message formatting
    - Configuration status boxes
    - Progress bars
    - Cycle headers
    - Abnormality gauges at different severity levels
    - Emergency alert styling
"""

from ui_utils import UI, Colors
import time

def demo():
    """
    Run the UI demonstration.

    Displays a complete walkthrough of all UI components in sequence:
    1. System headers with color styling
    2. Status messages (success, warning, error, info)
    3. Configuration summary box
    4. Progress bar animation
    5. Cycle header format
    6. Abnormality gauges (20%, 40%, 60%, 85%)
    7. Emergency alert banner

    This demo simulates the visual experience of the actual monitoring
    system without requiring user input or running the health algorithms.

    Example:
        $ python3 demo_ui.py
        ════════════════════════════════════════════════════════════
                  PERSONAL SAFETY MONITORING SYSTEM
        ════════════════════════════════════════════════════════════
        ...
    """
    # Header
    UI.header("PERSONAL SAFETY MONITORING SYSTEM", Colors.BRIGHT_MAGENTA)

    # Subheader
    UI.subheader("⚙️  CONFIGURATION SETUP", Colors.BRIGHT_BLUE)

    # Success/Warning/Error messages
    UI.success("Configuration loaded successfully")
    UI.warning("Low battery detected")
    UI.error("Connection failed")
    UI.info("System initialized", "ℹ️")

    # Status box
    config_items = [
        f"{Colors.GREEN}Baseline Heart Rate:{Colors.RESET} 75 bpm",
        f"{Colors.GREEN}PIN Protection:{Colors.RESET} Enabled (1234)",
        f"{Colors.GREEN}Emergency Contacts:{Colors.RESET} 3 configured",
    ]
    UI.status_box("CONFIGURATION SUMMARY", config_items)

    # Progress bar
    print(f"\n{Colors.BOLD}Loading initial data:{Colors.RESET}")
    for i in range(1, 5):
        UI.progress_bar(i, 4)
        time.sleep(0.3)

    # Cycle header
    UI.cycle_header(5)

    # Abnormality gauges at different levels
    print(f"\n{Colors.BOLD}Abnormality Level Examples:{Colors.RESET}\n")

    print("Normal level (20%):")
    UI.abnormality_gauge(20)

    print("\nElevated level (40%):")
    UI.abnormality_gauge(40)

    print("\nHigh level (60%):")
    UI.abnormality_gauge(60)

    print("\nCritical level (85%):")
    UI.abnormality_gauge(85)

    # Alert
    print("\n" + Colors.BRIGHT_RED + Colors.BOLD + "!"*60)
    print("  🚨  EMERGENCY ALERT SENT TO PRE-SAVED CONTACTS  🚨  ".center(60))
    print("!"*60 + Colors.RESET)

    print(f"\n{Colors.BRIGHT_GREEN}Demo complete!{Colors.RESET}")
    print(f"{Colors.CYAN}The actual monitoring system will look similar to this.{Colors.RESET}\n")

if __name__ == "__main__":
    demo()
