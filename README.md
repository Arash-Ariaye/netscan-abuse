# Network Scan Detector

A Python script to detect and block fast network scans by monitoring outgoing TCP (SYN) and UDP (non-DNS) traffic. It identifies scans targeting multiple IPs in a `/24` range, blocks the destination range using `iptables`, and logs block/unblock events. The script runs as a background service using `systemd`.

اسکریپتی به زبان پایتون برای شناسایی و بلاک کردن اسکن‌های سریع شبکه با مانیتورینگ ترافیک خروجی TCP (SYN) و UDP (غیر DNS). این اسکریپت اسکن‌هایی که چندین IP در رنج `/24` را هدف قرار می‌دهند شناسایی کرده، رنج مقصد را با `iptables` بلاک می‌کند و رویدادهای بلاک و باز شدن را لاگ می‌کند. اسکریپت به‌صورت سرویس پس‌زمینه با `systemd` اجرا می‌شود.

---

## Features | ویژگی‌ها

- **Scan Detection**: Detects scans targeting 8 or more unique IPs in a `/24` range within 2 seconds.
- **Automatic Blocking**: Blocks detected ranges using `iptables` for 24 hours.
- **Minimal Logging**: Logs only block and unblock events to `/var/log/scan_detector.log`.
- **Background Execution**: Runs as a `systemd` service for continuous operation.
- **Whitelist Support**: Ignores specified IP ranges (e.g., `192.168.1.0/24`, `8.8.8.8/32`).
- **Optimized Performance**: Uses efficient regex and `tcpdump` buffer optimization (`-B 4096`).

- **شناسایی اسکن**: اسکن‌هایی که 8 یا بیشتر IP یکتا در رنج `/24` را در 2 ثانیه هدف قرار می‌دهند، شناسایی می‌کند.
- **بلاک خودکار**: رنج‌های شناسایی‌شده را با `iptables` به مدت 24 ساعت بلاک می‌کند.
- **لاگ مینیمال**: فقط رویدادهای بلاک و باز شدن را در `/var/log/scan_detector.log` ثبت می‌کند.
- **اجرای پس‌زمینه**: به‌صورت سرویس `systemd` برای عملکرد مداوم اجرا می‌شود.
- **پشتیبانی از لیست سفید**: رنج‌های IP مشخص (مثل `192.168.1.0/24`، `8.8.8.8/32`) را نادیده می‌گیرد.
- **عملکرد بهینه**: از regex کارآمد و بهینه‌سازی بافر `tcpdump` (`-B 4096`) استفاده می‌کند.

---

## Requirements | پیش‌نیازها

- **Operating System**: Linux (tested on Ubuntu/Debian)
- **Dependencies**: `tcpdump`, `iptables`, `python3`, `at`
- **Permissions**: Root access for running `tcpdump` and modifying `iptables`

- **سیستم‌عامل**: لینوکس (تست‌شده روی اوبونتو/دبیان)
- **وابستگی‌ها**: `tcpdump`، `iptables`، `python3`، `at`
- **سطح دسترسی**: دسترسی روت برای اجرای `tcpdump` و تغییر `iptables`

---

## Installation | نصب

1. **Install Dependencies | نصب وابستگی‌ها**:
   ```bash
   sudo apt-get update
   sudo apt-get install tcpdump iptables python3 at
