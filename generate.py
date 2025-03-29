import random
import string
import argparse
import time
import sys
import re
from colorama import Fore, Style, init
import pyperclip  # Library for clipboard functionality

# Initialize colorama
init(autoreset=True)

def generate_password(length=16, use_uppercase=True, use_lowercase=True, use_numbers=True, use_special=True):
    """Generate a secure random password with customizable options"""
    if length < 12:
        length = 12  # Silently enforce minimum length

    # Define character pools based on user preferences
    character_pool = ""
    if use_uppercase:
        character_pool += string.ascii_uppercase
    if use_lowercase:
        character_pool += string.ascii_lowercase
    if use_numbers:
        character_pool += string.digits
    if use_special:
        # Include only specific special characters
        allowed_specials = "!@#$%&_-?"
        character_pool += allowed_specials

    if not character_pool:
        # Fallback to lowercase if nothing is selected
        character_pool = string.ascii_lowercase

    # Ensure password meets specific requirements
    password = []
    if use_special:
        password.extend(random.choices("!@#$%&_-?", k=2))  # At least 2 special characters
    if use_uppercase:
        password.extend(random.choices(string.ascii_uppercase, k=4))  # At least 4 uppercase
    if use_lowercase:
        password.extend(random.choices(string.ascii_lowercase, k=4))  # At least 4 lowercase
    if use_numbers:
        password.extend(random.choices(string.digits, k=2))  # At least 2 numbers

    # Fill the rest of the password length with random characters
    remaining_length = length - len(password)
    if remaining_length > 0:
        password.extend(random.choices(character_pool, k=remaining_length))

    # Shuffle the password to randomize character order
    random.shuffle(password)
    return ''.join(password)

def generate_from_template(template):
    """Generate a password based on a template pattern
    
    Pattern characters:
    - U: Uppercase letter
    - L: Lowercase letter
    - D: Digit
    - S: Special character
    - X: Any character (uppercase, lowercase, digit, or special)
    
    Example: UULDDSSX = 2 uppercase, 2 lowercase, 2 digits, 1 special, 1 any
    """
    result = []
    pattern_map = {
        'U': string.ascii_uppercase,
        'L': string.ascii_lowercase,
        'D': string.digits,
        'S': "!@#$%&_-?",
        'X': string.ascii_uppercase + string.ascii_lowercase + string.digits + "!@#$%&_-?"
    }
    
    for char in template:
        if char in pattern_map:
            result.append(random.choice(pattern_map[char]))
        else:
            # Treat any other template character as a literal
            result.append(char)
    
    return ''.join(result)

def evaluate_password_strength(password):
    """
    Evaluate the strength of a password based on length, complexity, and character diversity
    Returns a score from 0-100 and a description
    """
    score = 0
    feedback = []
    
    # Score based on length (up to 40 points)
    length = len(password)
    if length >= 16:
        score += 40
        feedback.append("Good length")
    elif length >= 12:
        score += 30
        feedback.append("Acceptable length")
    else:
        score += 15
        feedback.append("Too short")
    
    # Score based on character types (up to 40 points)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for c in password)
    
    char_types = sum([has_upper, has_lower, has_digit, has_special])
    score += char_types * 10
    
    if not has_upper:
        feedback.append("Add uppercase letters")
    if not has_lower:
        feedback.append("Add lowercase letters")
    if not has_digit:
        feedback.append("Add numbers")
    if not has_special:
        feedback.append("Add special characters")
    
    # Score based on character diversity (up to 20 points)
    unique_chars = len(set(password))
    diversity_score = min(20, int(unique_chars / length * 20))
    score += diversity_score
    
    if unique_chars < length / 2:
        feedback.append("Add more variety of characters")
    
    # Determine strength description
    if score >= 90:
        strength = "Very Strong"
    elif score >= 70:
        strength = "Strong"
    elif score >= 50:
        strength = "Moderate"
    elif score >= 30:
        strength = "Weak"
    else:
        strength = "Very Weak"
    
    return score, strength, feedback

def display_password(password, show_strength=False, copy_to_clipboard=True, animate=False):
    """Display a generated password with optional strength evaluation and animation"""
    if animate:
        animate_password(password)
    else:
        print(Fore.GREEN + Style.BRIGHT + "Generated Password:")
        print(Fore.MAGENTA + Style.BRIGHT + f"{password}")
    
    if show_strength:
        score, strength, feedback = evaluate_password_strength(password)
        strength_color = Fore.GREEN if score >= 70 else (Fore.YELLOW if score >= 50 else Fore.RED)
        print(strength_color + f"Strength: {strength} ({score}/100)")
        
        if feedback:
            print(Fore.YELLOW + "Feedback:")
            for item in feedback:
                print(Fore.YELLOW + f" • {item}")
    
    if copy_to_clipboard:
        try:
            pyperclip.copy(password)
            print(Fore.YELLOW + "✓ Password copied to clipboard! " + Fore.GREEN + "[Ready to paste]")
        except Exception:
            print(Fore.YELLOW + "! Could not copy password to clipboard")

def animate_password(password):
    """Display the password with a typing animation effect"""
    print(Fore.GREEN + Style.BRIGHT + "Generated Password:")
    
    # First show scrambled characters
    scrambled = ['*' for _ in password]
    print(Fore.CYAN + ''.join(scrambled), end='\r')
    time.sleep(0.5)
    
    # Reveal one character at a time
    for i in range(len(password)):
        scrambled[i] = password[i]
        print(Fore.MAGENTA + Style.BRIGHT + ''.join(scrambled), end='\r')
        time.sleep(0.1)
    
    # Final reveal with a little extra emphasis
    print(Fore.MAGENTA + Style.BRIGHT + password + ' ' * 10)

def matrix_effect(password):
    """Display password with a matrix-like falling character effect"""
    print(Fore.GREEN + Style.BRIGHT + "Generating secure password...\n")
    
    # Matrix effect setup
    lines = 5
    width = max(len(password) + 10, 30)
    matrix = [['  ' for _ in range(width)] for _ in range(lines)]
    
    # Initial random characters in matrix
    for _ in range(3):
        for i in range(lines):
            for j in range(width):
                if random.random() > 0.8:
                    matrix[i][j] = random.choice(string.ascii_letters + string.digits + "!@#$%^&*")
        
        # Print matrix
        for line in matrix:
            print(Fore.GREEN + ''.join(line))
        time.sleep(0.1)
        # Move cursor back up
        print(f"\033[{lines}A", end='')
    
    # Reveal password in the middle of the matrix
    middle_row = lines // 2
    start_col = (width - len(password)) // 2
    
    for i in range(len(password)):
        for j in range(3):  # Flash a few times
            matrix[middle_row][start_col + i] = Fore.WHITE + Style.BRIGHT + password[i] + Fore.GREEN + Style.NORMAL
            
            # Print matrix
            for line in matrix:
                print(''.join(line))
            time.sleep(0.05)
            
            # Move cursor back up
            print(f"\033[{lines}A", end='')
    
    # Final display
    for line in matrix:
        print(''.join(line))
    print("\n" + Fore.MAGENTA + Style.BRIGHT + "Password: " + password)
    print()

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Generate secure random passwords')
    
    parser.add_argument('-l', '--length', type=int, default=16,
                        help='Password length (default: 16, minimum: 12)')
    
    parser.add_argument('-n', '--number', type=int, default=1,
                        help='Number of passwords to generate (default: 1)')
    
    parser.add_argument('--no-uppercase', action='store_true',
                        help='Exclude uppercase letters')
    
    parser.add_argument('--no-lowercase', action='store_true',
                        help='Exclude lowercase letters')
    
    parser.add_argument('--no-numbers', action='store_true',
                        help='Exclude numbers')
    
    parser.add_argument('--no-special', action='store_true',
                        help='Exclude special characters')
    
    parser.add_argument('--no-clipboard', action='store_true',
                        help='Do not copy password to clipboard')
    
    parser.add_argument('-e', '--evaluate', action='store_true',
                        help='Show password strength evaluation')
                        
    parser.add_argument('-s', '--save', type=str, metavar='FILENAME',
                        help='Save generated passwords to file')
    
    parser.add_argument('-t', '--template', type=str, metavar='PATTERN',
                        help='Use pattern template (U=uppercase, L=lowercase, D=digit, S=special, X=any)')
                        
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Run in interactive mode')
    
    parser.add_argument('-a', '--animate', action='store_true',
                        help='Show animated password reveal')
                        
    parser.add_argument('-m', '--matrix', action='store_true',
                        help='Show password with matrix effect animation')
    
    # Check if any arguments were provided
    if len(sys.argv) > 1:
        return parser.parse_args()
    else:
        # Return default values if no args provided
        return parser.parse_known_args([])[0]

def save_passwords_to_file(passwords, filename):
    """Save generated passwords to a file"""
    try:
        with open(filename, 'w') as file:
            for i, password in enumerate(passwords, 1):
                file.write(f"Password {i}: {password}\n")
        return True
    except Exception as e:
        print(Fore.RED + f"Error saving passwords to file: {e}")
        return False

def print_header():
    """Print the application header"""
    header = """
    ╔═══════════════════════════════════════════════════════╗
    ║                 PASSWORD GENERATOR                    ║
    ╚═══════════════════════════════════════════════════════╝"""
    print(Fore.CYAN + Style.BRIGHT + header)

def run_interactive_mode():
    """Run the password generator in interactive mode"""
    print(Fore.YELLOW + "\nPassword Generator Interactive Mode")
    print(Fore.YELLOW + "=" * 50)
    
    # Get user preferences
    try:
        # Password length
        while True:
            try:
                length = int(input(Fore.CYAN + "Enter password length (min 12, default 16): " + Style.RESET_ALL) or "16")
                if length < 12:
                    print(Fore.RED + "Password length must be at least 12. Using 12.")
                    length = 12
                break
            except ValueError:
                print(Fore.RED + "Please enter a valid number")
        
        # Character types
        use_uppercase = input(Fore.CYAN + "Include uppercase letters? (Y/n): " + Style.RESET_ALL).lower() != 'n'
        use_lowercase = input(Fore.CYAN + "Include lowercase letters? (Y/n): " + Style.RESET_ALL).lower() != 'n'
        use_numbers = input(Fore.CYAN + "Include numbers? (Y/n): " + Style.RESET_ALL).lower() != 'n'
        use_special = input(Fore.CYAN + "Include special characters? (Y/n): " + Style.RESET_ALL).lower() != 'n'
        
        if not any([use_uppercase, use_lowercase, use_numbers, use_special]):
            print(Fore.RED + "You must include at least one character type. Using all types.")
            use_uppercase = use_lowercase = use_numbers = use_special = True
        
        # Number of passwords
        while True:
            try:
                num_passwords = int(input(Fore.CYAN + "Number of passwords to generate (default 1): " + Style.RESET_ALL) or "1")
                if num_passwords < 1:
                    print(Fore.RED + "Must generate at least 1 password. Using 1.")
                    num_passwords = 1
                break
            except ValueError:
                print(Fore.RED + "Please enter a valid number")
        
        # Password evaluation
        show_strength = input(Fore.CYAN + "Show password strength evaluation? (y/N): " + Style.RESET_ALL).lower() == 'y'
        
        # Copy to clipboard
        copy_to_clipboard = input(Fore.CYAN + "Copy password to clipboard? (Y/n): " + Style.RESET_ALL).lower() != 'n'
        
        # Animation options
        animate = input(Fore.CYAN + "Show animated reveal? (y/N): " + Style.RESET_ALL).lower() == 'y'
        
        # Save to file
        save_to_file = input(Fore.CYAN + "Save passwords to file? (y/N): " + Style.RESET_ALL).lower() == 'y'
        filename = None
        if save_to_file:
            filename = input(Fore.CYAN + "Enter filename: " + Style.RESET_ALL)
            if not filename:
                save_to_file = False
                print(Fore.YELLOW + "No filename provided. Passwords will not be saved.")
        
        # Generate the passwords
        print(Fore.YELLOW + "\nGenerating passwords...")
        generated_passwords = []
        for i in range(num_passwords):
            password = generate_password(
                length=length,
                use_uppercase=use_uppercase,
                use_lowercase=use_lowercase,
                use_numbers=use_numbers,
                use_special=use_special
            )
            generated_passwords.append(password)
        
        # Display the passwords
        print(Fore.YELLOW + f"\nGenerated {num_passwords} password(s):")
        print(Fore.YELLOW + "=" * 50)
        
        for i, password in enumerate(generated_passwords, 1):
            if num_passwords > 1:
                print(Fore.CYAN + f"\nPassword {i}:")
            
            # Only copy the last password to clipboard (or if only generating one)
            copy_current = (i == num_passwords) and copy_to_clipboard
            display_password(password, show_strength, copy_current, animate and (i == num_passwords))
        
        # Save passwords to file if requested
        if save_to_file and filename:
            if save_passwords_to_file(generated_passwords, filename):
                print(Fore.GREEN + f"\nPasswords saved to {filename}")
        
        return True
    
    except KeyboardInterrupt:
        print(Fore.RED + "\nOperation cancelled by user.")
        return False

def is_valid_template(template):
    """Check if the template contains at least one of each required char type"""
    if len(template) < 12:
        return False
    
    has_upper = 'U' in template
    has_lower = 'L' in template
    has_digit = 'D' in template
    has_special = 'S' in template
    
    # If X is present, it can substitute for missing requirements
    x_count = template.count('X')
    required_count = 4 - sum([has_upper, has_lower, has_digit, has_special])
    
    return x_count >= required_count

if __name__ == "__main__":
    print_header()
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Check for help request
    if '--help' in sys.argv or '-h' in sys.argv:
        # Help will be automatically displayed by argparse
        exit(0)
    
    # Check if interactive mode was requested
    if args.interactive:
        success = run_interactive_mode()
        if success:
            print(Fore.YELLOW + "\n" + "=" * 50)
            print(Fore.CYAN + "Thank you for using the Password Generator Tool!")
        exit(0)
    
    # Process arguments and generate passwords
    try:
        # Process template pattern if provided
        if args.template:
            if not is_valid_template(args.template):
                print(Fore.YELLOW + "Warning: Template may not produce secure passwords.")
                print(Fore.YELLOW + "Ensure it includes U (uppercase), L (lowercase), D (digit), and S (special) characters.")
                
            # Generate using template
            generated_passwords = []
            for i in range(args.number):
                password = generate_from_template(args.template)
                generated_passwords.append(password)
        else:
            # Normal password generation
            if args.length < 12:
                print(Fore.YELLOW + "Password length less than 12 is not recommended.")
                print(Fore.YELLOW + "Adjusting to minimum length of 12.")
                args.length = 12
                
            # Check if at least one character type is enabled
            if args.no_uppercase and args.no_lowercase and args.no_numbers and args.no_special:
                print(Fore.YELLOW + "Warning: At least one character type must be enabled.")
                print(Fore.YELLOW + "Using lowercase letters as default.")
                args.no_lowercase = False
            
            # Generate the passwords
            generated_passwords = []
            for i in range(args.number):
                password = generate_password(
                    length=args.length,
                    use_uppercase=not args.no_uppercase,
                    use_lowercase=not args.no_lowercase,
                    use_numbers=not args.no_numbers,
                    use_special=not args.no_special
                )
                generated_passwords.append(password)
        
        # Display the passwords
        print(Fore.YELLOW + f"\nGenerated {args.number} password(s):")
        print(Fore.YELLOW + "=" * 50)
        
        # Special matrix effect
        if args.matrix and args.number == 1:
            matrix_effect(generated_passwords[0])
            # Copy to clipboard
            if not args.no_clipboard:
                try:
                    pyperclip.copy(generated_passwords[0])
                    print(Fore.YELLOW + "✓ Password copied to clipboard! " + Fore.GREEN + "[Ready to paste]")
                except Exception:
                    print(Fore.YELLOW + "! Could not copy password to clipboard")
        else:
            # Regular display
            for i, password in enumerate(generated_passwords, 1):
                if args.number > 1:
                    print(Fore.CYAN + f"\nPassword {i}:")
                
                # Only copy the last password to clipboard (or if only generating one)
                copy_to_clipboard = (i == args.number) and not args.no_clipboard
                animate = args.animate and (i == args.number)
                display_password(password, args.evaluate, copy_to_clipboard, animate)
        
        # Save passwords to file if requested
        if args.save:
            if save_passwords_to_file(generated_passwords, args.save):
                print(Fore.GREEN + f"\nPasswords saved to {args.save}")
        
        print(Fore.YELLOW + "\n" + "=" * 50)
        print(Fore.CYAN + "Thank you for using the Password Generator Tool!")
        
    except ValueError as e:
        print(Fore.RED + Style.BRIGHT + f"Error: {e}")
    except KeyboardInterrupt:
        print(Fore.RED + "\nOperation cancelled by user.")