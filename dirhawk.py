# dirhawk.py

import argparse
import asyncio
from utils import print_banner, load_wordlist
from scanner import run_scanner

def main():
    print_banner("HAWK")

    parser = argparse.ArgumentParser(description="DirHawk - Advanced Directory Fuzzer")
    parser.add_argument("-u", "--url", required=True, help="Target base URL (e.g. https://example.com)")
    parser.add_argument("-w", "--wordlist", help="Custom wordlist file path")
    parser.add_argument("-e", "--extensions", help="Comma separated file extensions to fuzz (e.g. php,html,txt)")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Number of concurrent threads (default: 20)")
    parser.add_argument("-o", "--output", default="results.txt", help="File to save results (default: results.txt)")
    parser.add_argument("--retries", type=int, default=1, help="Retries for failed requests (default: 1)")
    parser.add_argument("--rate", type=int, default=100, help="Requests per second rate limit (default: 100)")
    parser.add_argument("--status", help="Comma separated HTTP status codes to filter results (e.g. 200,403). Shows all if omitted.")

    args = parser.parse_args()

    extensions = args.extensions.split(",") if args.extensions else []
    wordlist_path = args.wordlist if args.wordlist else "wordlists/default.txt"

    # Parse status filter
    if args.status:
        try:
            status_codes = [int(code.strip()) for code in args.status.split(",") if code.strip()]
        except ValueError:
            print("[!] Invalid status codes in --status argument.")
            return
    else:
        status_codes = None  # means show all

    wordlist = load_wordlist(wordlist_path)
    if not wordlist:
        print("[!] Wordlist is empty or not found. Exiting.")
        return

    asyncio.run(
        run_scanner(
            url=args.url,
            wordlist=wordlist,
            extensions=extensions,
            threads=args.threads,
            output_file=args.output,
            retries=args.retries,
            rate_limit=args.rate,
            status_filter=status_codes,
        )
    )

if __name__ == "__main__":
    main()
