import subprocess
import platform
import re
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
from tabulate import tabulate

# Initialize colorama for cross-platform colored output
init()

# Xeovo VPN server info
xeovo_vpn_info = {
    "al":      ("au.gw.xeovo.com", "Albania", "Tirana"),
    "au":      ("au.gw.xeovo.com", "Australia", "Sydney"),
    "ca":      ("ca.gw.xeovo.com", "Canada", "Montreal"),
    "ch":      ("ch.gw.xeovo.com", "Switzerland", "Zurich"),
    "de":      ("ch.gw.xeovo.com", "Germany", "Falkenstein"),
    "fi":      ("fi.gw.xeovo.com", "Finland", "Helsinki"),
    "fr":      ("fr.gw.xeovo.com", "France", "Paris"),
    "jp":      ("jp.gw.xeovo.com", "Japan", "Tokyo"),
    "lu":      ("lu.gw.xeovo.com", "Luxembourg", "Roost"),
    "lv":      ("lv.gw.xeovo.com", "Latvia", "Riga"),
    "nl":      ("nl.gw.xeovo.com", "Netherlands", "Amsterdam"),
    "no":      ("no.gw.xeovo.com", "Norway", "Sandefjord"),
    "pl":      ("pl.gw.xeovo.com", "Poland", "Warsaw"),
    "ro":      ("ro.gw.xeovo.com", "Romania", "Iasi"),
    "se":      ("se.gw.xeovo.com", "Sweden", "Stockholm"),
    "sg":      ("sg.gw.xeovo.com", "Singapore", "Singapore"),
    "ua":      ("ua.gw.xeovo.com", "Ukraine", "Kyiv"),
    "uk":      ("uk.gw.xeovo.com", "United Kingdom", "London"),
    "us-lv":   ("us-lv.gw.xeovo.com", "United States", "Las Vegas"),
    "us-mia":  ("us-mia.gw.xeovo.com", "United States", "Miami"),
    "us-nyc":  ("us-nyc.gw.xeovo.com", "United States", "New York")
}

# Function to fetch server load dynamically
def fetch_server_load_data():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }
        response = requests.get("https://status.xeovo.com/", timeout=10, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find the VPN Servers section
        vpn_section = None
        for header in soup.find_all(["h2", "h3", "h4"], string=re.compile("VPN Servers", re.I)):
            vpn_section = header
            break
        
        if not vpn_section:
            return {}
        
        # Find the table container
        server_data = {}
        table = soup.find("table", class_="vpngw")
        if not table:
            return {}
        
        # Parse table rows
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) >= 2:
                location = cells[0].get_text(strip=True)
                status_span = cells[1].find("span", class_="text")
                if status_span:
                    load = status_span.get_text(strip=True)
                    if location and load:
                        server_data[location] = load
        
        return server_data
    except (requests.RequestException, AttributeError):
        return {}

# Function to get server load
def get_server_load(country, city, server_load_data):
    # Handle special cases for United States, United Kingdom, and Singapore servers
    if country == "United States":
        key = f"USA, {city}"
    elif country == "United Kingdom":
        key = f"UK, {city}"
    elif city == "Singapore":
        key = country
    else:
        key = f"{country}, {city}"
    
    load = server_load_data.get(key, "N/A")
    # Extract percentage if load is a percentage string, else return as is
    if load.endswith("% load"):
        return load.replace(" load", "")
    return load

# Function to color latency
def color_latency(latency):
    if latency == float("inf"):
        return Fore.RED + "timeout" + Style.RESET_ALL
    latency_ms = f"{latency:.1f} ms"
    if latency < 50:
        return Fore.GREEN + latency_ms + Style.RESET_ALL
    elif latency < 100:
        return Fore.YELLOW + latency_ms + Style.RESET_ALL
    else:
        return Fore.RED + latency_ms + Style.RESET_ALL

# Function to color load
def color_load(load):
    if load == "N/A":
        return load
    if load == "DOWN":
        return Fore.RED + "DOWN" + Style.RESET_ALL
    try:
        load_value = int(load.replace("%", ""))
        if load_value < 30:
            return Fore.GREEN + load + Style.RESET_ALL
        elif load_value < 60:
            return Fore.YELLOW + load + Style.RESET_ALL
        else:
            return Fore.RED + load + Style.RESET_ALL
    except ValueError:
        return load

# Ping function
def ping(host):
    system = platform.system().lower()
    param = "-n" if system == "windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", param, "1", host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=3
        )
        output = result.stdout
        if system == "windows":
            match = re.search(r"(\d+)", output.split(" = ")[-1])
        else:
            match = re.search(r"time=(\d+\.?\d*) ms", output)
        if match:
            return float(match.group(1))
    except subprocess.TimeoutExpired:
        return float("inf")
    return float("inf")

# Main function to run the script
def main():
    # Fetch server load data once
    server_load_data = fetch_server_load_data()

    # Ping all servers and collect results
    results = []
    for code, (host, country, city) in xeovo_vpn_info.items():
        latency = ping(host)
        load = get_server_load(country, city, server_load_data)
        results.append((latency, country, city, host, load))

    # Prepare table data
    table_data = []
    for idx, (latency, country, city, host, load) in enumerate(results, 1):
        colored_status = color_latency(latency)
        colored_load = color_load(load)
        table_data.append([idx, country, city, host, colored_status, colored_load])

    # Print results using tabulate
    headers = ["#", "Country", "City", "Host", "Latency", "Load"]
    print("\nXeovo VPN Server Latency and Load List:\n")
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

if __name__ == "__main__":
    main()
