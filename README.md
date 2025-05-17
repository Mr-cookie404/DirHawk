<div align="center">
  <h1>🦅 DIRHAWK</h1>
  <h3>A Powerful and Advanced CLI-based Directory Fuzzing Tool for Cybersecurity Professionals</h3>
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python Badge">
  <img src="https://img.shields.io/badge/platform-linux%20%7C%20windows-lightgrey" alt="Platform Badge">
  <img src="https://img.shields.io/github/license/yourusername/dirhawk" alt="License Badge">
</div>

---

## 📌 Overview

**DirHawk** is a fast, accurate, and user-friendly directory fuzzing tool developed for penetration testers, bug bounty hunters, and cybersecurity professionals. It helps discover hidden endpoints and directories on a web server by fuzzing the URLs using custom and built-in wordlists.

DirHawk offers advanced features like status code filtering, rate limiting, retry logic, colored CLI output, and result saving to ensure optimal performance and precision.

---

## 🚀 Features

- ✅ **Blazing fast multithreaded scanning**
- ✅ **Filter by HTTP status codes (e.g., only 200 OK)**
- ✅ **Supports custom & default wordlists**
- ✅ **Output results to file**
- ✅ **Rate limiting and retry logic**
- ✅ **Real-time progress display**
- ✅ **Beautiful ASCII banner (H A W K)**
- ✅ **Cross-platform support (Linux & Windows)**

---

## 🛠️ Requirements

- Python 3.8 or higher

### Install dependencies:

```bash
pip install -r requirements.txt

🔹 Basic Scan

python dirhawk.py -u https://example.com
🔹 Use a Custom Wordlist

python dirhawk.py -u https://example.com -w wordlists/custom.txt
🔹 Filter by Status Code (Only 200 OK)

python dirhawk.py -u https://example.com --filter 200
🔹 Set Rate Limit (1 request/sec)

python dirhawk.py -u https://example.com --rate 1
🔹 Save Results to a Custom File

python dirhawk.py -u https://example.com -o my_output.txt
🔹 Show Help

python dirhawk.py --help


🖥️ Sample Output

[200] https://example.com/admin
[403] https://example.com/.htaccess
[301] https://example.com/login → https://example.com/login/