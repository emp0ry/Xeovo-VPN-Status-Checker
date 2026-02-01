<p align="center">
  <img src="https://xeovo.com/static/images/logo.svg" width="510" alt="Xeovo Logo">
</p>

<h1 align="center">Xeovo VPN Status Checker</h1>

<p align="center">
  A cross-platform CLI tool that pings Xeovo VPN gateways and shows a clean, colorized table with
  <strong>real latency</strong> and <strong>server load</strong>.
  <br>
  Works on <strong>Windows</strong>, <strong>Linux</strong>, and <strong>macOS</strong>.
</p>

<p align="center">
  <a href="https://github.com/emp0ry/Xeovo-VPN-Status-Checker/releases/latest">
    <img src="https://img.shields.io/github/v/release/emp0ry/Xeovo-VPN-Status-Checker?logo=github&color=5865F2" alt="Latest Release">
  </a>
  <a href="https://img.shields.io/github/downloads/emp0ry/Xeovo-VPN-Status-Checker/total?color=ff6d00&label=Total%20Downloads">
    <img src="https://img.shields.io/github/downloads/emp0ry/Xeovo-VPN-Status-Checker/total?color=ff6d00&label=Total%20Downloads" alt="Total Downloads">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white" alt="Python Version">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/github/license/emp0ry/Xeovo-VPN-Status-Checker?color=00C853" alt="License: MIT">
  </a>
</p>


---

## 🚀 What This Does

This script:

- Pings Xeovo VPN servers (e.g., `au.gw.xeovo.com`) to measure **real latency**
- Scrapes **server load** from <a href="https://status.xeovo.com/">status.xeovo.com</a>
- Prints a **colored, tabulated** status list in your terminal
- Uses OS-specific ping flags for Windows / Linux / macOS

> ✅ Tip: For *real geographic latency*, run this **outside** the VPN.  

---

## ✨ Features

- **Ping Servers**: Reliable latency measurement with robust parsing (Windows + Unix).
- **Real-Time Load**: Pulls load % from the Xeovo status page.
- **Colored Output**:
  - **Latency**: Green (fast), Yellow (medium), Red (slow/timeout)
  - **Load**: Green (low), Yellow (medium), Red (high / DOWN / N/A)
- **Special Cases**: Supports Xeovo naming like `USA, ...`, `UK, ...`, and `Singapore`.
- **Clean Table Output**: Uses `tabulate` to render a bordered table.
- **No Sorting**: Keeps a predefined server order.
- **Cross-Platform**: Works on Windows / Linux / macOS.

---

## 📦 Requirements

- **Python 3.6+**
- Packages from `requirements.txt`:
  - `requests`
  - `beautifulsoup4`
  - `colorama`
  - `tabulate`
- System `ping` command:
  - Pre-installed on Windows/macOS
  - On Linux it may require installing `iputils-ping`

---

## 🛠️ Installation

### 1) Clone the Repository
```bash
git clone https://github.com/emp0ry/Xeovo-VPN-Status-Checker.git
cd Xeovo-VPN-Status-Checker
````

### 2) Install Python (if not installed)

#### Windows

Download from: [https://www.python.org](https://www.python.org)
(make sure to check **“Add Python to PATH”**)

#### Linux

Ubuntu / Debian:

```bash
sudo apt-get update
sudo apt-get install -y python3
```

CentOS / RHEL:

```bash
sudo yum install -y python3
```

#### macOS

```bash
brew install python3
```

Verify:

```bash
python --version
# or
python3 --version
```

### 3) Install the Ping Command (Linux only, if missing)

Ubuntu / Debian:

```bash
sudo apt-get install -y iputils-ping
```

CentOS / RHEL:

```bash
sudo yum install -y iputils
```

### 4) Install Dependencies

```bash
pip install -r requirements.txt
```

If you get permission errors:

```bash
pip install -r requirements.txt --user
```

---

## ▶️ Usage

Run:

```bash
python main.py
# or
python3 main.py
```

On Linux, if ICMP ping requires root:

```bash
sudo python3 main.py
```

The script will:

* Fetch load data from `status.xeovo.com`
* Ping each Xeovo VPN server
* Print a table with **Country / City / Host / Latency / Load**

---

## 📋 Example Output

```
Xeovo VPN Server Latency and Load List:

+----------------+------------+---------------------+-----------+--------+
| Country        | City       | Host                | Latency   | Load   |
+================+============+=====================+===========+========+
| Albania        | Tirana     | al.gw.xeovo.com     | 77.0 ms   | 45%    |
+----------------+------------+---------------------+-----------+--------+
| Australia      | Sydney     | au.gw.xeovo.com     | 331.0 ms  | 0%     |
+----------------+------------+---------------------+-----------+--------+
| Brazil         | São Paulo  | br.gw.xeovo.com     | 287.0 ms  | 0%     |
+----------------+------------+---------------------+-----------+--------+
| ---            | ---        | ---                 | ---       | ---    |
+----------------+------------+---------------------+-----------+--------+
| United States  | Las Vegas  | us-lv.gw.xeovo.com  | 198.0 ms  | 1%     |
+----------------+------------+---------------------+-----------+--------+
| United States  | Miami      | us-mia.gw.xeovo.com | 168.0 ms  | 0%     |
+----------------+------------+---------------------+-----------+--------+
| United States  | New York   | us-nyc.gw.xeovo.com | 138.0 ms  | 0%     |
+----------------+------------+---------------------+-----------+--------+
```

> Note: In the terminal, values are colored (green/yellow/red).
> Some servers may show `N/A` if the status page format changes or a server is missing.

---

## 💡 Platform Notes

### Windows

* Works out of the box
* Colored output supported (via `colorama`)

### Linux

* You may need `iputils-ping`
* Some systems require `sudo` for ping
  Alternative (not recommended unless you understand it):

  ```bash
  sudo chmod u+s /bin/ping
  ```

### macOS

* Use `python3` if `python` points to Python 2

---

## 🧰 Troubleshooting

### Load shows `N/A`

* Check if <a href="https://status.xeovo.com/">status.xeovo.com</a> is reachable
* Xeovo may change page structure → scraper may need updates

### Ping fails / shows timeout

* Check your firewall / ICMP restrictions
* On Linux try `sudo`
* Make sure DNS is working and hostnames resolve

---

## 💖 Support the Project

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/emp0ry)

---

## 📜 License

Released under the [MIT License](LICENSE).

---

## 🙌 Acknowledgments

* Built with Python, `requests`, `beautifulsoup4`, `colorama`, and `tabulate`
* Status data sourced from <a href="https://status.xeovo.com/">Xeovo Status Page</a>
