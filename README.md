# GenR8 - Password Generator Tool

A powerful command-line utility for generating secure random passwords.

## Features

- Generate strong random passwords with a single command
- Customize passwords with optional arguments (uppercase, lowercase, numbers, special characters)
- Generate multiple passwords at once
- Password strength evaluation
- Copy generated passwords to clipboard automatically
- Save generated passwords to a file
- Fun animated password reveals
- Interactive guided mode

## Installation

1. Make sure you have Python 3.6 or higher installed
2. Clone this repository or download the source code
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
Simply run without any arguments to generate a secure password:

```bash
python genr8.py
```

This will generate a 16-character password with all character types and copy it to your clipboard.

### Command Line Arguments (All Optional)

| Argument | Description |
|----------|-------------|
| `-l, --length LENGTH` | Password length (default: 16, minimum: 12) |
| `-n, --number NUMBER` | Number of passwords to generate (default: 1) |
| `--no-uppercase` | Exclude uppercase letters |
| `--no-lowercase` | Exclude lowercase letters |
| `--no-numbers` | Exclude numbers |
| `--no-special` | Exclude special characters |
| `--no-clipboard` | Do not copy password to clipboard |
| `-e, --evaluate` | Show password strength evaluation |
| `-s, --save FILENAME` | Save generated passwords to file |
| `-a, --animate` | Show animated password reveal |
| `-m, --matrix` | Show password with Matrix-style animation effect |
| `-t, --template PATTERN` | Use pattern template (U=uppercase, L=lowercase, D=digit, S=special, X=any) |
| `-i, --interactive` | Run in interactive mode |
| `-h, --help` | Show help message |

### Examples

Generate a 20-character password:
```bash
python genr8.py -l 20
```

Generate a password without special characters (for websites that don't allow them):
```bash
python genr8.py --no-special
```

Generate 5 passwords:
```bash
python genr8.py -n 5
```

Generate a password with animated reveal:
```bash
python genr8.py -a
```

Generate a password with Matrix-style effect:
```bash
python genr8.py -m
```

Generate a password and evaluate its strength:
```bash
python genr8.py -e
```

Generate 3 passwords and save them to a file:
```bash
python genr8.py -n 3 -s passwords.txt
```

Create a password with a specific pattern:
```bash
python genr8.py -t "UUULLLDDSXXXX"
```

Run in interactive guided mode:
```bash
python genr8.py -i
```

## Security Notes

- Passwords are generated using Python's random module with strong methods
- Generated passwords are designed to meet modern security requirements
- For maximum security, it's recommended to use passwords of at least 16 characters with all character types enabled