# Network Scan Detector

A lightweight Python script to detect and block fast network scans by monitoring outgoing TCP (SYN) and UDP (non-DNS) traffic. It blocks `/24` ranges with 8+ unique IPs in 2 seconds using `iptables` and logs block/unblock events. Runs as a `systemd` service.

اسکریپت سبک پایتون برای شناسایی و بلاک کردن اسکن‌های سریع شبکه با مانیتورینگ ترافیک خروجی TCP (SYN) و UDP (غیر DNS). رنج‌های `/24` با 8 یا بیشتر IP یکتا در 2 ثانیه با `iptables` بلاک می‌شن و رویدادهای بلاک و باز شدن لاگ می‌شن. به‌صورت سرویس `systemd` اجرا می‌شه.

---

## Installation | نصب

Run this one-liner to install everything automatically:

```bash
curl -sL https://raw.githubusercontent.com/Arash-Ariaye/netscan-abuse/refs/heads/main/install.sh | sudo bash && rm -f install.sh
```
---
## Features | ویژگی‌ها

- Detects scans targeting 8+ unique IPs in a `/24` range in 2 seconds.
- Blocks detected ranges for 24 hours using `iptables`.
- Logs only block (`Blok shod`) and unblock (`Baz shod`) events in `/var/log/scan_detector.log`.
- Runs in the background as a `systemd` service.
- Supports whitelisted IP ranges (e.g., `192.168.1.0/24`, `8.8.8.8/32`).

- اسکن‌هایی با 8 یا بیشتر IP یکتا در رنج `/24` در 2 ثانیه شناسایی می‌کنه.
- رنج‌های شناسایی‌شده رو به مدت 24 ساعت با `iptables` بلاک می‌کنه.
- فقط رویدادهای بلاک (`Blok shod`) و باز شدن (`Baz shod`) رو در `/var/log/scan_detector.log` لاگ می‌کنه.
- به‌صورت پس‌زمینه با سرویس `systemd` اجرا می‌شه.
- از رنج‌های IP سفید (مثل `192.168.1.0/24`، `8.8.8.8/32`) پشتیبانی می‌کنه.

---

## Requirements | پیش‌نیازها

- **OS**: Linux (Ubuntu/Debian recommended)
- **Dependencies**: `tcpdump`, `iptables`, `python3`, `at`
- **Permissions**: Root access

- **سیستم‌عامل**: لینوکس (اوبونتو/دبیان توصیه می‌شه)
- **وابستگی‌ها**: `tcpdump`، `iptables`، `python3`، `at`
- **دسترسی**: روت

---

