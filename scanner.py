# scanner.py

import asyncio
import httpx
import async_timeout
from rich.console import Console

console = Console()

async def get_baseline_404(session, base_url):
    test_path = "/this_path_definitely_does_not_exist_12345"
    url = base_url.rstrip("/") + test_path
    try:
        async with async_timeout.timeout(10):
            response = await session.get(url, follow_redirects=True)
            content = response.content
            snippet = content[:100]
            return {
                "status_code": response.status_code,
                "content_length": len(content),
                "body_snippet": snippet,
            }
    except Exception:
        return None

def is_similar_response(resp, baseline, threshold=0.95):
    if not baseline:
        return False

    if resp.status_code != baseline["status_code"]:
        return False

    length1 = len(resp.content)
    length2 = baseline["content_length"]
    similarity = min(length1, length2) / max(length1, length2) if max(length1, length2) > 0 else 0

    if similarity < threshold:
        return False

    snippet1 = resp.content[:len(baseline["body_snippet"])]
    if snippet1 == baseline["body_snippet"]:
        return True

    return False

async def run_scanner(url, wordlist, extensions, threads, output_file, retries, rate_limit, status_filter=None):
    semaphore = asyncio.Semaphore(rate_limit)
    found = []

    headers = {"User-Agent": "DirHawk Scanner"}

    async with httpx.AsyncClient() as session:
        baseline = await get_baseline_404(session, url)
        if baseline:
            console.print("[*] Baseline 404 response recorded.", style="cyan")
        else:
            console.print("[!] Could not get baseline 404 response. False positives may increase.", style="yellow")

        async def scan_url(full_url):
            for attempt in range(retries + 1):
                try:
                    async with semaphore:
                        async with async_timeout.timeout(10):
                            response = await session.get(full_url, headers=headers, follow_redirects=True)
                            if is_similar_response(response, baseline):
                                break

                            if status_filter is None or response.status_code in status_filter:
                                entry = f"[{response.status_code}] {full_url}"
                                found.append(entry)
                                # Print with colors
                                if response.status_code == 200:
                                    console.print(entry, style="bold green")
                                elif response.status_code == 403:
                                    console.print(entry, style="yellow")
                                elif response.status_code in [301, 302]:
                                    console.print(entry, style="cyan")
                                else:
                                    console.print(entry)
                            break
                except Exception as e:
                    if attempt == retries:
                        console.print(f"[!] Failed: {full_url} after {retries} retries", style="bold red")

        tasks = []
        for word in wordlist:
            paths = [word] + [f"{word}.{ext}" for ext in extensions]
            for path in paths:
                full_url = url.rstrip('/') + '/' + path.strip('/')
                tasks.append(scan_url(full_url))

        await asyncio.gather(*tasks)

    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for item in found:
                    f.write(item + "\n")
            console.print(f"\n[✔] Results saved to: {output_file}", style="bold blue")
        except Exception as e:
            console.print(f"[!] Error writing to file: {e}", style="bold red")
