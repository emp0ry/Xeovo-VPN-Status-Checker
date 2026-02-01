import subprocess
import platform
import re
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

# Xeovo VPN server info
xeovo_vpn_info = {
    "al":      ("al.gw.xeovo.com", "Albania", "Tirana"),
    "au":      ("au.gw.xeovo.com", "Australia", "Sydney"),
    "br":      ("br.gw.xeovo.com", "Brazil", "São Paulo"),
    "ca":      ("ca.gw.xeovo.com", "Canada", "Montreal"),
    "ch":      ("ch.gw.xeovo.com", "Switzerland", "Zurich"),
    "de":      ("de.gw.xeovo.com", "Germany", "Nuremberg"),
    "fi":      ("fi.gw.xeovo.com", "Finland", "Helsinki"),
    "fr":      ("fr.gw.xeovo.com", "France", "Paris"),
    "jp":      ("jp.gw.xeovo.com", "Japan", "Tokyo"),
    "lu":      ("lu.gw.xeovo.com", "Luxembourg", "Roost"),
    "lv":      ("lv.gw.xeovo.com", "Latvia", "Riga"),
    "nl":      ("nl.gw.xeovo.com", "Netherlands", "Amsterdam"),
    "no":      ("no.gw.xeovo.com", "Norway", "Sandefjord"),
    "pl":      ("pl.gw.xeovo.com", "Poland", "Warsaw"),
    "ro":      ("ro.gw.xeovo.com", "Romania", "Bucharest"),
    "se":      ("se.gw.xeovo.com", "Sweden", "Stockholm"),
    "sg":      ("sg.gw.xeovo.com", "Singapore", "Singapore"),
    "ua":      ("ua.gw.xeovo.com", "Ukraine", "Kyiv"),
    "uk":      ("uk.gw.xeovo.com", "United Kingdom", "London"),
    "us-lv":   ("us-lv.gw.xeovo.com", "United States", "Las Vegas"),
    "us-mia":  ("us-mia.gw.xeovo.com", "United States", "Miami"),
    "us-nyc":  ("us-nyc.gw.xeovo.com", "United States", "New York"),
}

STATUS_URL = "https://status.xeovo.com/"

IGNORED_LINES = {
    "VPN Servers",
    "Stealth Proxy Servers",
    "Service",
    "Service Availability",
    "Past Incidents",
    "WireGuard, AmneziaWG and OpenVPN protocols.",
    "Shadowsocks, VMess, VLESS and Trojan protocols.",
    "P2P",
    "CN",
}

SERVER_CODE_RE = re.compile(r"^[A-Z]{2}(?:-[A-Z]{2})?-\d+$")  # e.g. AL-2, US-LV-3, UK-1
PERCENT_RE = re.compile(r"^\d{1,3}%$")


def _normalize_lines_from_html(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n", strip=True)
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def _find_section(lines: list[str], start_title: str, end_title: str) -> list[str]:
    def find_idx(title: str):
        t = title.strip().lower()
        for i, ln in enumerate(lines):
            if ln.strip().lower() == t:
                return i
        return None

    s = find_idx(start_title)
    e = find_idx(end_title)
    if s is None or e is None or e <= s:
        return []
    return lines[s + 1 : e]


def _looks_like_location(line: str) -> bool:
    if line in IGNORED_LINES:
        return False
    if "●" in line:
        return False
    if SERVER_CODE_RE.match(line):
        return False
    if PERCENT_RE.match(line):
        return False
    if "," in line:
        return True
    if line == "Singapore":
        return True
    return False


def fetch_server_load_data() -> dict[str, str]:
    """
    Returns mapping like:
      "Finland, Helsinki" -> "72%"
      "USA, Las Vegas"    -> "8%"
      "Singapore"         -> "0%"
    """
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/129.0.0.0 Safari/537.36"
            )
        }
        r = requests.get(STATUS_URL, timeout=15, headers=headers)
        r.raise_for_status()

        lines = _normalize_lines_from_html(r.text)
        vpn_lines = _find_section(lines, "VPN Servers", "Stealth Proxy Servers")
        if not vpn_lines:
            return {}

        data = {}
        i = 0
        while i < len(vpn_lines):
            ln = vpn_lines[i]

            if _looks_like_location(ln):
                location = ln

                # Find FIRST percentage after location (skip Operational/P2P/etc.)
                j = i + 1
                found = None
                while j < len(vpn_lines):
                    nxt = vpn_lines[j]
                    if _looks_like_location(nxt):
                        break
                    if PERCENT_RE.match(nxt):
                        found = nxt
                        break
                    j += 1

                if found:
                    data[location] = found

                i = j
                continue

            i += 1

        return data
    except requests.RequestException:
        return {}


def get_server_load(country: str, city: str, server_load_data: dict[str, str]) -> str:
    # Xeovo labels: "USA, ..." and "UK, ..." on the status page
    if country == "United States":
        key = f"USA, {city}"
    elif country == "United Kingdom":
        key = f"UK, {city}"
    elif city == "Singapore":
        key = "Singapore"
    else:
        key = f"{country}, {city}"

    return server_load_data.get(key, "N/A")


def ping(host: str) -> float:
    """
    Robust ping parser:
      - Windows: parse reply line time=XXms or time<1ms first
      - Unix: parse time=XX ms
      - Fallback: parse avg from summary
      - Treat 0.0 as invalid (except <1ms => 0.5ms)
    """
    system = platform.system().lower()

    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", "2500", host]
    else:
        # Linux/macOS
        cmd = ["ping", "-c", "1", "-W", "2", host] if system == "linux" else ["ping", "-c", "1", host]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=4
        )
        out = (result.stdout or "") + "\n" + (result.stderr or "")

        # Windows: Reply time=XXms or time<1ms
        if system == "windows":
            m = re.search(r"time[=<]\s*(\d+)\s*ms", out, re.IGNORECASE)
            if m:
                val = float(m.group(1))
                if val <= 0:
                    # time<1ms sometimes appears as 0 in summaries; represent as 0.5ms
                    return 0.5
                return val

            # Windows fallback: Average = XXms (no space before ms sometimes)
            m = re.search(r"Average\s*=\s*(\d+)\s*ms", out, re.IGNORECASE)
            if m:
                val = float(m.group(1))
                return val if val > 0 else float("inf")

        # Unix: time=XX ms
        m = re.search(r"time[=<]\s*(\d+(?:\.\d+)?)\s*ms", out, re.IGNORECASE)
        if m:
            val = float(m.group(1))
            return val if val > 0 else float("inf")

        # Unix fallback: rtt min/avg/max/... = a/b/c/d
        m = re.search(r"=\s*\d+(?:\.\d+)?/(\d+(?:\.\d+)?)/", out)
        if m:
            val = float(m.group(1))
            return val if val > 0 else float("inf")

    except subprocess.TimeoutExpired:
        return float("inf")

    return float("inf")


def main():
    server_load_data = fetch_server_load_data()

    results = []
    for _, (host, country, city) in xeovo_vpn_info.items():
        latency = ping(host)
        load = get_server_load(country, city, server_load_data)
        latency_str = "timeout" if latency == float("inf") else f"{latency:.1f} ms"
        results.append((country, city, host, latency_str, load))

    headers = ["Country", "City", "Host", "Latency", "Load"]

    # Prevent console wrapping by limiting wide columns (tabulate will wrap within the cell)
    print("\nXeovo VPN Server Latency and Load List:\n")
    print(tabulate(
        results,
        headers=headers,
        tablefmt="grid",
        disable_numparse=True,
        maxcolwidths=[18, 14, 26, 12, 6]
    ))


if __name__ == "__main__":
    main()
    print()
    input("Press Enter to continue... ")
