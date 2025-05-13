#!/bin/bash

# File: install.sh
# Gharardad: Script baraye nasb khodkar scan_detector
# Link GitHub: https://github.com/Arash-Ariaye/netscan-abuse

# Rang-ha baraye log rooye safhe
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Log function baraye namayesh payam
log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Error function baraye khataye mortabet
error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] Khataye: $1${NC}"
    exit 1
}

# Check kardan dastresi root
if [ "$EUID" -ne 0 ]; then
    error "In script bayad ba dastresi root ejra shavad. Lotfan az sudo estefade konid."
fi

# Update kardan package-ha
log "Dar hal update package-ha..."
apt-get update -y || error "Khataye update package-ha"

# Nasb pishniaz-ha
log "Dar hal nasb pishniaz-ha (tcpdump, iptables, python3, at)..."
apt-get install -y tcpdump iptables python3 at || error "Khataye nasb pishniaz-ha"

# Check kardan nasb shodan pishniaz-ha
for pkg in tcpdump iptables python3 at; do
    if ! command -v $pkg &> /dev/null; then
        error "Package $pkg nasb nashod."
    else
        log "Package $pkg ba movaffaghiat nasb shod."
    fi
done

# Download kardan script-ha az GitHub
log "Dar hal download scan_detector.py..."
curl -o /usr/local/bin/scan_detector.py https://raw.githubusercontent.com/Arash-Ariaye/netscan-abuse/refs/heads/main/scan_detector.py || error "Khataye download scan_detector.py"
log "Dar hal download unblock.sh..."
curl -o /usr/local/bin/unblock.sh https://raw.githubusercontent.com/Arash-Ariaye/netscan-abuse/refs/heads/main/unblock.sh || error "Khataye download unblock.sh"

# Dadan dastresi ejra be script-ha
log "Dadan dastresi ejra be script-ha..."
chmod +x /usr/local/bin/scan_detector.py /usr/local/bin/unblock.sh || error "Khataye dadan dastresi ejra"

# Check kardan file-ha
for file in /usr/local/bin/scan_detector.py /usr/local/bin/unblock.sh; do
    if [ ! -f "$file" ]; then
        error "File $file vojud nadarad."
    else
        log "File $file ba movaffaghiat download shod."
    fi
done

# Sakht file service systemd
log "Dar hal sakht service systemd..."
cat > /etc/systemd/system/scan-detector.service << EOL
[Unit]
Description=Network Scan Detector
After=network.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/scan_detector.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOL

# Check kardan sakht service
if [ ! -f "/etc/systemd/system/scan-detector.service" ]; then
    error "File service scan-detector.service sakhte nashod."
else
    log "File service scan-detector.service ba movaffaghiat sakhte shod."
fi

# Reload kardan systemd va faal kardan service
log "Reload kardan systemd..."
systemctl daemon-reload || error "Khataye reload systemd"
log "Faal kardan service scan-detector..."
systemctl enable scan-detector.service || error "Khataye faal kardan service"
log "Ejra kardan service scan-detector..."
systemctl start scan-detector.service || error "Khataye ejra kardan service"

# Check kardan vaziat service
log "Check kardan vaziat service..."
if systemctl is-active --quiet scan-detector.service; then
    log "${GREEN}Service scan-detector ba movaffaghiat dar hal ejrast!${NC}"
else
    error "Service scan-detector ejra nashod. Lotfan log-ha ra ba 'journalctl -u scan-detector' check konid."
fi

# Payam nahayi
log "${GREEN}Nasb ba movaffaghiat tamam shod!${NC}"
log "Log-haye blok va baz shodan dar /var/log/scan_detector.log zakhire mishavand."
log "Baraye test, mitavanid az 'nmap -sU 102.193.214.0/24' ya 'nmap -sS 102.193.214.0/24' estefade konid."
