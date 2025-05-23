# 🌐 Xeovo VPN Status Checker

A Python script that pings Xeovo VPN servers, fetches their real-time server load from [status.xeovo.com](https://status.xeovo.com/), and displays the results in a colored, tabulated format. The script is **cross-platform**, running on **Windows**, **Linux**, and **macOS**.

## 🛠️ PS
**⚠️ Load not working now.**

## 🚀 Features
- **Ping Servers**: Measures latency to Xeovo VPN servers (e.g., `au.gw.xeovo.com`).
- **Real-Time Load**: Scrapes server load data from https://status.xeovo.com/.
- **Colored Output**:
  - Latency: Green (<50 ms), Yellow (50–100 ms), Red (>100 ms or timeout).
  - Load: Green (<30%), Yellow (30–60%), Red (>60% or DOWN).
- **Special Cases**: Handles unique location names (e.g., "Singapore", "UK, London" instead of "United Kingdom, London").
- **Tabulated Display**: Uses `tabulate` with `fancy_grid` for clean, bordered tables.
- **No Sorting**: Lists servers in a predefined order.
- **Cross-Platform**: Adapts to Windows, Linux, and macOS for ping commands and terminal output.

## 📦 Requirements
- Python 3.6 or higher
- Required Python packages (listed in `requirements.txt`):
  - `requests`
  - `beautifulsoup4`
  - `colorama`
  - `tabulate`
- The `ping` command (pre-installed on Windows and macOS; may need installation on Linux)

## 🛠️ Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/emp0ry/Xeovo-VPN-Status-Checker.git
   cd Xeovo-VPN-Status-Checker
   ```

2. **Install Python** (if not already installed):
   - **Windows**: Download from [python.org](https://www.python.org/) or use `choco install python`.
   - **Linux**: Install via package manager:
     - Ubuntu/Debian: `sudo apt-get install python3`
     - CentOS/RHEL: `sudo yum install python3`
   - **macOS**: Use Homebrew: `brew install python3` (or pre-installed on recent versions).
   - Verify: `python3 --version` or `python --version`.

3. **Install the Ping Command** (Linux only, if missing):
   - Ubuntu/Debian: `sudo apt-get install iputils-ping`
   - CentOS/RHEL: `sudo yum install iputils`

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   If permission issues occur:
   ```bash
   pip install -r requirements.txt --user
   ```

5. **Ensure Internet Access**:
   - The script requires access to https://status.xeovo.com/ and VPN servers for pinging.

## ▶️ Usage
Run the script with:
```bash
python main.py
```
On Linux, if ping permissions are restricted:
```bash
sudo python main.py
```

The script will:
- Fetch server load data from https://status.xeovo.com/.
- Ping each Xeovo VPN server.
- Display a table with server details, latency, and load.

### 📋 Example Output
```
Xeovo VPN Server Latency and Load List:

╒═════╤════════════════╤════════════╤═════════════════════╤═══════════╤════════╕
│   # │ Country        │ City       │ Host                │ Latency   │ Load   │
╞═════╪════════════════╪════════════╪═════════════════════╪═══════════╪════════╡
│   1 │ Australia      │ Sydney     │ au.gw.xeovo.com     │ 331.0 ms  │ 16%    │
├─────┼────────────────┼────────────┼─────────────────────┼───────────┼────────┤
│   2 │ Canada         │ Montreal   │ ca.gw.xeovo.com     │ 142.0 ms  │ 4%     │
├─────┼────────────────┼────────────┼─────────────────────┼───────────┼────────┤
│   3 │ Switzerland    │ Zurich     │ ch.gw.xeovo.com     │ 70.0 ms   │ 17%    │
├─────┼────────────────┼────────────┼─────────────────────┼───────────┼────────┤
│   4 │ Finland        │ Helsinki   │ fi.gw.xeovo.com     │ 84.0 ms   │ 51%    │
├─────┼────────────────┼────────────┼─────────────────────┼───────────┼────────┤
│ ... │ ...            │ ...        │ ...                 │ ...       │ ...    │
├─────┼────────────────┼────────────┼─────────────────────┼───────────┼────────┤
│  16 │ United Kingdom │ London     │ uk.gw.xeovo.com     │ 65.0 ms   │ 32%    │
├─────┼────────────────┼────────────┼─────────────────────┼───────────┼────────┤
│  17 │ United States  │ Las Vegas  │ us-lv.gw.xeovo.com  │ 211.0 ms  │ 14%    │
├─────┼────────────────┼────────────┼─────────────────────┼───────────┼────────┤
│  18 │ United States  │ Miami      │ us-mia.gw.xeovo.com │ 173.0 ms  │ 4%     │
├─────┼────────────────┼────────────┼─────────────────────┼───────────┼────────┤
│  19 │ United States  │ New York   │ us-nyc.gw.xeovo.com │ 140.0 ms  │ 20%    │
╘═════╧════════════════╧════════════╧═════════════════════╧═══════════╧════════╛
```
*Note*: Latency and load values are colored (green/yellow/red) in the terminal but shown here as plain text. Some servers may show "N/A" if not listed on the status page.

## 💡 Platform-Specific Notes
- **Windows**:
  - Works out of the box with Python 3.6+ and `ping` (pre-installed).
  - Ensure `colorama` is installed for colored output in Command Prompt or PowerShell.
- **Linux**:
  - Install `iputils-ping` if `ping` is missing.
  - May require `sudo` for `ping` due to ICMP restrictions. Alternatively, set ping permissions:
    ```bash
    sudo chmod u+s /bin/ping
    ```
- **macOS**:
  - Python 3 and `ping` are typically pre-installed.
  - Use `python3` to run the script if `python` points to Python 2.

## 🧰 Troubleshooting
- **Loads Show "N/A"**:
  - Verify internet access and that https://status.xeovo.com/ is reachable.
  - Check if the page structure has changed by inspecting `<table class="vpngw">` in the browser.
  - Share the output table for further debugging.
- **Ping Failures**:
  - Ensure `ping` is installed and accessible.
  - Check firewall settings to allow ICMP packets.
  - On Linux, use `sudo` or adjust `ping` permissions if errors occur.
- **Dependency Issues**:
  - Ensure `requirements.txt` is in the project directory.
  - Run `pip install -r requirements.txt --user` for permission errors.
  - Verify Python 3.6+ (`python3 --version` or `python --version`).

## ☕ Donation
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/emp0ry)

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙌 Acknowledgments
- Built with Python, `requests`, `beautifulsoup4`, `colorama`, and `tabulate`.
- Data sourced from [Xeovo VPN Status Page](https://status.xeovo.com/).
