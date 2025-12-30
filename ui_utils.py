"""
UI Utilities for enhanced terminal display with colors and formatting
"""

class Colors:
    """ANSI color codes for terminal output"""
    # Basic colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright colors
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'

    # Styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'


class UI:
    """Helper functions for pretty terminal output"""

    @staticmethod
    def header(text: str, color=Colors.CYAN):
        """Print a header with border"""
        border = "=" * 60
        print(f"\n{color}{Colors.BOLD}{border}")
        print(f"{text.center(60)}")
        print(f"{border}{Colors.RESET}\n")

    @staticmethod
    def subheader(text: str, color=Colors.BLUE):
        """Print a subheader"""
        print(f"\n{color}{Colors.BOLD}{'─' * 60}")
        print(f"{text}")
        print(f"{'─' * 60}{Colors.RESET}\n")

    @staticmethod
    def success(text: str):
        """Print success message"""
        print(f"{Colors.BRIGHT_GREEN}✓ {text}{Colors.RESET}")

    @staticmethod
    def warning(text: str):
        """Print warning message"""
        print(f"{Colors.BRIGHT_YELLOW}⚠️  {text}{Colors.RESET}")

    @staticmethod
    def error(text: str):
        """Print error message"""
        print(f"{Colors.BRIGHT_RED}✗ {text}{Colors.RESET}")

    @staticmethod
    def alert(text: str):
        """Print alert message with red background"""
        print(f"\n{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD} 🚨 {text} 🚨 {Colors.RESET}\n")

    @staticmethod
    def info(text: str, icon="ℹ️"):
        """Print info message"""
        print(f"{Colors.CYAN}{icon}  {text}{Colors.RESET}")

    @staticmethod
    def status_box(title: str, items: list):
        """Print a status box with items"""
        width = 60
        print(f"\n{Colors.BOLD}┌{'─' * (width-2)}┐")
        print(f"│ {title.ljust(width-4)} │")
        print(f"├{'─' * (width-2)}┤")
        for item in items:
            # Handle colored items
            visible_len = len(item.replace(Colors.RESET, '').replace(Colors.GREEN, '')
                             .replace(Colors.YELLOW, '').replace(Colors.RED, '')
                             .replace(Colors.CYAN, '').replace(Colors.BOLD, ''))
            padding = width - 4 - visible_len
            print(f"│ {item}{' ' * padding} │")
        print(f"└{'─' * (width-2)}┘{Colors.RESET}\n")

    @staticmethod
    def progress_bar(current: int, total: int, width: int = 40):
        """Display a simple progress bar"""
        filled = int((current / total) * width)
        bar = '█' * filled + '░' * (width - filled)
        percent = int((current / total) * 100)
        print(f"{Colors.CYAN}[{bar}] {percent}%{Colors.RESET}")

    @staticmethod
    def cycle_header(cycle_num: int, color=Colors.BRIGHT_CYAN):
        """Print a cycle header"""
        print(f"\n{color}{Colors.BOLD}╔{'═' * 58}╗")
        print(f"║{f'CYCLE {cycle_num}'.center(58)}║")
        print(f"╚{'═' * 58}╝{Colors.RESET}")

    @staticmethod
    def abnormality_gauge(percentage: float):
        """Display abnormality as a visual gauge"""
        # Determine color based on severity
        if percentage < 30:
            color = Colors.BRIGHT_GREEN
            status = "NORMAL"
        elif percentage < 45:
            color = Colors.YELLOW
            status = "ELEVATED"
        elif percentage < 70:
            color = Colors.BRIGHT_YELLOW
            status = "HIGH"
        else:
            color = Colors.BRIGHT_RED
            status = "CRITICAL"

        # Create gauge
        filled = int(percentage / 2)  # 50 chars = 100%
        bar = '█' * filled + '░' * (50 - filled)

        print(f"\n{Colors.BOLD}Abnormality Level:{Colors.RESET}")
        print(f"{color}[{bar}] {int(percentage)}% - {status}{Colors.RESET}")
