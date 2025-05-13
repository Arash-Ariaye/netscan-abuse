#!/bin/bash
NETWORK=$1
LOG_FILE="/var/log/scan_detector.log"

# Hazf ghanoon iptables
sudo iptables -D OUTPUT -d "$NETWORK" -j DROP

# Log baz shodan range
echo "$(date): Baz shod: $NETWORK dar $(date)" >> "$LOG_FILE"
