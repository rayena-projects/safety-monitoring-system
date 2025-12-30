"""
Emergency alert notification system.

This module handles sending alerts to pre-configured emergency contacts
when a safety concern is detected. In production, this would integrate
with SMS, push notifications, and phone call APIs.
"""

from ui_utils import Colors


class AlertSystem:
    """
    Manages emergency contact notifications.

    This class is responsible for alerting pre-saved emergency contacts
    when the monitoring system detects a potential safety issue. In this
    simulation, it prints to console; in production, it would send real
    SMS messages, push notifications, or initiate phone calls.

    Production Integration Points:
        - Twilio API for SMS and voice calls
        - Firebase Cloud Messaging for push notifications
        - Email via SendGrid or similar service
        - Integration with emergency services (911 API where available)

    Note:
        Emergency contacts would be configured during user onboarding and
        stored securely in the user's profile.
    """

    def send_alert(self):
        """
        Send emergency alert to all pre-configured contacts.

        Displays a simulated alert notification. In production, this would:
        1. Send SMS to each emergency contact with user's location
        2. Send push notifications to contacts' phones
        3. Optionally initiate automated phone calls
        4. Log the alert event for safety records

        The alert message includes:
            - Timestamp of the alert
            - User's current GPS location (in production)
            - Nature of the safety concern
            - Link to real-time monitoring dashboard (in production)

        Example:
            >>> alert_system = AlertSystem()
            >>> alert_system.send_alert()
            🚨 EMERGENCY ALERT SENT TO PRE-SAVED CONTACTS 🚨
            ✓ Mother - (123) 456-7890
            ...
        """
        print("\n" + Colors.BRIGHT_RED + Colors.BOLD + "!"*60)
        print("  🚨  EMERGENCY ALERT SENT TO PRE-SAVED CONTACTS  🚨  ".center(60))
        print("!"*60 + Colors.RESET)
        print(f"\n{Colors.YELLOW}Notifying contacts...{Colors.RESET}")
        print(f"  {Colors.BRIGHT_GREEN}✓{Colors.RESET} Mother - (123) 456-7890")
        print(f"  {Colors.BRIGHT_GREEN}✓{Colors.RESET} Father - (123) 456-7891")
        print(f"  {Colors.BRIGHT_GREEN}✓{Colors.RESET} Trusted Friend - (123) 456-7892")
        print(f"\n{Colors.CYAN}Alert Message:{Colors.RESET}")
        print(f"  {Colors.BOLD}'Safety concern detected. Please check on me.'{Colors.RESET}")
        print(f"\n{Colors.BRIGHT_RED}" + "!"*60 + Colors.RESET + "\n")
