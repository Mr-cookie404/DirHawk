# utils.py

from rich.console import Console

console = Console()

def print_banner(name="HAWK"):
    banner = r"""
H     H      A      W       W     K   K
H     H     A A     W       W     K  K 
HHHHHHH    AAAAA    W   W   W     KKK  
H     H   A     A   W  W W  W     K  K 
H     H  A       A   W W   W      K   K
"""
    console.print(banner, style="bold cyan")

def load_wordlist(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    except FileNotFoundError:
        console.print(f"[red][!] Wordlist file not found: {path}[/red]")
        return []
    except Exception as e:
        console.print(f"[red][!] Error loading wordlist: {e}[/red]")
        return []
