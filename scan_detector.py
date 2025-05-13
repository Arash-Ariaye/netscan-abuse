#!/usr/bin/env python3
import subprocess
import re
import time
import ipaddress

# Tanzimat
THRESHOLD = 8  # Tedad minimum IP-haye mokhtalef dar yek range /24
SCAN_WINDOW = 2  # Maximum baze zamani baraye tashkhis scan sari (sanie)
INTERFACE = "eth0"  # Rabete shabake
SERVER_IP = $(hostname -I | awk '{print $1}')  # IP server
LOG_FILE = "/var/log/scan_detector.log"
BLOCKED_RANGES = set()  # Baraye jelogiri az blok tekrari
WHITELIST = {"192.168.1.0/24", "10.0.0.0/24", "8.8.8.8/32", "8.8.4.4/32"}  # List sefid
BLOCK_DURATION = 86400  # Moddat zaman blok (24 saat)
UNBLOCK_SCRIPT = "/usr/local/bin/unblock.sh"  # Script hazf blok

def log_message(message):
    """Zakhire log faghat dar file (bedun namayesh ruye safhe)"""
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.ctime()}: {message}\n")

def get_traffic():
    """Jamavari traffic khoruji TCP va UDP be surat zende (bedun DNS)"""
    cmd = f"sudo tcpdump -i {INTERFACE} -nn -tt -B 4096 'src host {SERVER_IP} and ((tcp[13] & 2 != 0) or (udp and not port 53))'"
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    return process

def parse_traffic(process):
    """Tajzie traffic zende va shomaresh IP-haye moghsad ba tavajoh be zamanbandi"""
    packets = {}  # Zakhire packet-ha: {network: [(timestamp, dst_ip), ...]}
    timestamp_regex = re.compile(r"(\d+\.\d+)")
    ip_regex = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*>\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
    
    while True:
        try:
            line = process.stdout.readline().strip()
            if not line:
                stderr = process.stderr.readline()
                if stderr:
                    log_message(f"Khataye tcpdump: {stderr}")
                log_message("Data bishtar az tcpdump nist")
                break
            
            timestamp_match = timestamp_regex.search(line)
            ip_match = ip_regex.search(line)
            if timestamp_match and ip_match:
                timestamp = float(timestamp_match.group(1))
                src_ip = ip_match.group(1)
                dst_ip = ip_match.group(2)
                
                # Mohasebe range /24 baraye IP moghsad
                network = str(ipaddress.IPv4Network(dst_ip + "/24", strict=False))
                
                # Nadide gereftan packet-haye range blok shode
                if network in BLOCKED_RANGES:
                    continue
                
                # Zakhire packet
                if network not in packets:
                    packets[network] = []
                packets[network].append((timestamp, dst_ip))
            
            # Paksazi packet-haye ghadimi
            for network in list(packets.keys()):
                packets[network] = [
                    (ts, ip) for (ts, ip) in packets[network]
                    if timestamp - ts <= SCAN_WINDOW
                ]
                if not packets[network]:
                    del packets[network]
            
            # Tahlil scan-haye sari
            detected_networks = set()
            for network in packets:
                if network in BLOCKED_RANGES or network in WHITELIST:
                    continue
                unique_ips = set(ip for (_, ip) in packets[network])
                if len(unique_ips) >= THRESHOLD:
                    detected_networks.add(network)
            
            if detected_networks:
                return detected_networks, process
        
        except KeyboardInterrupt:
            log_message("Script tavasot karbar ghat shod")
            process.terminate()
            return set(), process
        except Exception as e:
            log_message(f"Khataye tajzie traffic: {e}")
            continue
        
        time.sleep(0.005)  # Kam kardan masraf CPU

def block_network(network):
    """Blok kardan range /24 moghsad ba iptables dar zanjire OUTPUT"""
    if network in BLOCKED_RANGES or network in WHITELIST:
        return
    try:
        cmd = f"sudo iptables -A OUTPUT -d {network} -j DROP"
        subprocess.run(cmd, shell=True, check=True)
        BLOCKED_RANGES.add(network)
        # Log blok shodan range
        log_message(f"Blok shod: {network} dar {time.ctime()}")
        # Barnamerizi hazf ghanoon ba script unblock.sh
        subprocess.run(
            f"echo '{UNBLOCK_SCRIPT} {network}' | at now + 24 hours",
            shell=True
        )
    except subprocess.CalledProcessError as e:
        log_message(f"Khataye blok kardan {network}: {e}")

def main():
    try:
        # Shoru ferayand tcpdump
        process = get_traffic()
        while True:
            # Tahlil traffic zende
            detected_networks, process = parse_traffic(process)
            
            # Blok kardan range-haye mashkok
            for network in detected_networks:
                block_network(network)
            
            # Barresi vaziat ferayand tcpdump
            if process.poll() is not None:
                log_message("Ferayand tcpdump payan yaft, restart...")
                process = get_traffic()
            
            time.sleep(0.1)  # Jelogiri az masraf bishtar az had CPU
    
    except KeyboardInterrupt:
        log_message("Script tavasot karbar ghat shod")
        process.terminate()

if __name__ == "__main__":
    main()
