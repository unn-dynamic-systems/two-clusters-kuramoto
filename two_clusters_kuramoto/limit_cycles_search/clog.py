class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

ENDC = '\033[0m'

color_to_magic_map = {
    "underline": '\033[4m',
    "header": '\033[95m',
    'okblue': '\033[94m',
    'okgreen': '\033[92m',
    'okcyan': '\033[96m'
}

def log_str(message, color):
    return f"{color_to_magic_map.get(color, '')}{message}{ENDC}"

def log(message, color):
    print(log_str(message, color))

 
