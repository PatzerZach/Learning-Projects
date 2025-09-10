import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from scapy.all import IP, TCP, sr1, send
import ssl
from tabulate import tabulate

def tcp_syn_scan(port, target):
    ip = IP(dst=target)
    tcp = TCP(dport=port, flags="S")
    response = sr1(ip/tcp, timeout=5, verbose=0)
    
    if response is None:
        return (f"{port}/tcp", "Filtered", None, None, None)
    
    if response.haslayer(TCP):
        flags = response.getlayer(TCP).flags
        if flags == 0x12:
            send(ip/TCP(dport=port, flags="R"), verbose=0)
            
            service, version = banner_grabbing(port, target)
            os_info = os_fingerprinting(response)
            
            return (f"{port}/tcp", "Open", service, version, os_info)
        elif flags == 0x14:
            return (f"{port}/tcp", "Closed", None, None, None)
    return (f"{port}/tcp", "Unknown", None, None, None)

def tcp_ack_scan(port, target):
    ip = IP(dst=target)
    tcp = TCP(dport=port, flags="A")
    response = sr1(ip/tcp, timeout=5, verbose=0)
    
    service = socket.getservbyport(port, "tcp")
    
    if response is None:
        return (f"{port}/tcp", "Filtered", service, None, None)
    
    if response.haslayer(TCP):
            return (f"{port}/tcp", "Unfiltered", service, None, None)
    return (f"{port}/tcp", "Unknown", service, None, None)

def tcp_connect_scan(port, target):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        result = s.connect_ex((target, port))
        
        if result == 0:
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(1024).decode(errors="ignore").strip()
            service, version = banner_grabbing(port, target)
            s.close()
                
            return f"{port}/tcp", "Open", service, {version}, "Unknown"
        
        else:
            s.close()
            return f"{port}/tcp", "Closed", None, None, None
        
    except socket.timeout:
        return f"{port}/tcp", "Filtered", None, None, None
    except Exception:
        return f"{port}/tcp", "Error", None, None, None
    
def udp_scan(port, target):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(5)
        s.sendto(b"Hello", (target, port))
        
        try:
            data, _ = s.recvfrom(1024)
            service, version = banner_grabbing(port, target)
            return (f"{port}/udp", "Open", service, version, None)
        except socket.timeout:
            service = socket.getservbyport(port, "udp")
            return (f"{port}/udp", "Open|Filtered", service, None, None)
    except socket.error as e:
        return (f"{port}/udp", "Closed", None, None, None)
    finally:
        s.close()
            


def banner_grabbing(port, target):
    try:
        s = socket.socket()
        s.settimeout(5)
        
        if port in [443, 8443, 993, 995, 465]:
            context = ssl.create_default_context()
            ssock = context.wrap_socket(s, server_hostname=target)
            ssock.connect((target, port))
            
            cert = ssock.getpeercert()
            ssock.close()
            
            subject = dict(x[0] for x in cert.get("subject", []))
            issued_to = subject.get("commonName", "Unknown")
            
            issuer = dict(x[0] for x in cert.get("issuer", []))
            issued_by = issuer.get("commonName", "Unknown")
            
            return "https", f"SSL Cert: {issued_to} (Issuer: {issued_by})"
        
        else:
            s.connect((target, port))
        
            try:
                banner = s.recv(1024).decode(errors="ignore").strip()
            except socket.timeout:
                banner = ""
                
            if port == 80:
                s.send(b"HEAD / HTTP/1.0\r\nHost: %b\r\n\r\n" % target.encode())
                try:
                    http_response = s.recv(2048).decode(errors="ignore")
                except socket.timeout:
                    http_response = ""
                    
                if http_response:
                    headers = http_response.split("\r\n")
                    server_line = next((h for h in headers if h.lower().startswith("server:")), None)
                    if server_line:
                        banner = server_line
            s.close()
                
            if not banner:
                return socket.getservbyport(port, "tcp"), "Unknown"
            
            banner_line = banner.split("\n")[0]
            service = socket.getservbyport(port, "tcp")
            return service, banner_line
        
    except Exception:
        return "Unknown", "Unknown"

def os_fingerprinting(response):
    ttl = response[IP].ttl if response.haslayer(IP) else None
    window = response[TCP].window
    options = dict(response[TCP].options) if response[TCP].options else {}
    has_ts = "Timestamp" in options
    if ttl == 64 and has_ts:
        return "Linux"
    elif ttl == 65 and window == 29200 and has_ts and ("MMS", 1460) in options:
        return "100% Linux"
    elif ttl == 64 and window == 29200 or ("MMS", 1460) in options:
        return "Linux (Ubuntu/Debian?)"
    elif ttl == 64 and not has_ts:
        return "Linux/Unix Like"
    elif ttl == 128 or ("MSS", 1460):
        return "Windows"
    return "Unknown"

def port_parser(inputs):
    port_input = inputs.replace(" ", "")
    ports = set()
    if port_input == "all":
        ports.update(range(0, 65536))
    else:
        for part in port_input.split(","):
            if "-" in part:
                start, end = part.split("-")
                ports.update(range(int(start), int(end)+1))
            else:
                ports.add(int(part))
            
    return sorted(ports)

def hostname_target(input):
    if all(part.isdigit() for part in input.split(".")):
        output = input
    else:
        output = socket.gethostbyname(input)
    return output

def run_scan(scan, ports, target, outputs, max_threads=100):
    results = {}
    table = []
    with ThreadPoolExecutor(max_threads) as executor:
        futures = [executor.submit(scan, port, target) for port in ports]
        
        for future in as_completed(futures):
            port, state, service, version, os_hint = future.result()
            results[port] = {
                "state": state,
                "service": service,
                "version": version,
                "os_hit": os_hint
            }
            if outputs == "y":
                if state == "Open":
                    table.append([port, state, f"{service or ''} {version or ''}", os_hint or ''])
            else:
                table.append([port, state, f"{service or ''} {version or ''}", os_hint or ''])
    headers = ["PORT", "STATE", "SERVICE", "OS"]
    print(tabulate(table, headers=headers, tablefmt="pretty"))
    
    return results

def main():
    print('\n')
    print("="*60)
    print('Welcome to the port scanner')
    print('='*60, "\n")
    scan_options = [
        "TCP SYN Scan \t(Sends SYN packets to probe ports; open ports reply with SYN-ACK (stealthier than full connect))",
        "TCP ACK Scan \t(Sends ACK packets to detect firewall rules (open vs. filtered), not port states directly)",
        "TCP Connect Scan \t(Attempts a full TCP handshake; simpler but more detectable)",
        "UDP Scan \t(Sends UDP datagrams; open ports often give no reply, while closed ports send ICMP errors)",
        "SCTP INIT Scan \t(Probes SCTP services by sending INIT chunks; responses reveal open/closed state)",
        "TCP NULL Scan \t(Sends TCP packets with no flags set; responses (or lack thereof) hint at port state)",
        "FIN Scan \t(Sends TCP packets with only the FIN flag; closed ports usually send RST back)",
        "Xmas Scan \t(Sends packets with FIN, PSH, and URG set; used to evade filters and detect open ports)",
        "TCP Window Scan \t(Like ACK scan but inspects TCP window size field to infer open/closed state)",
        "TCP Maimon Scan \t(Sends FIN/ACK probes that some systems ignore on open ports, revealing state)",
        "SCTP COOKIE ECHO Scan \t(Sends COOKIE-ECHO chunks to detect open SCTP asociations more stealithily)",
        "TCP Idle Scan \t(Uses a 'zombie' host's IP ID field to scan target indiretly (stealthy and spoofed))",
        "IP Protocol Scan \t(Sends raw IP packets with varying protocol numbers to see which are supported)",
        "PING Request \t(Sends ICMP Echo requests to check if the host is alive/reachable)"
    ]
    for i, scan in enumerate(scan_options, start=1):
        print(f"{i}. {scan}")
    
    choice = int(input("Please enter the scan number: "))
    port_input = input("Enter the ports you would like to scan (443), (1,2,3,4,5), (1-443), (1-443, 445-690), (all): " )
    ports = port_parser(port_input)
    target_original = str(input("Enter the target IP address or URL: "))
    target = hostname_target(target_original)
    threads = int(input("How many threads would you like to use for multithreading (MAX: 50): "))
    outputs = str(input("Would you like to only display open ports (y/n)? "))
    
    scan_functions = {
        1: tcp_syn_scan,
        2: tcp_ack_scan,
        3: tcp_connect_scan,
        4: udp_scan
    }
    
    # scan_functions = {
    #     1: tcp_syn_scan,
    #     2: tcp_ack_scan,
    #     3: tcp_connect_scan,
    #     4: udp_scan,
    #     5: sctp_init_scan,
    #     6: tcp_null_scan,
    #     7: fin_scan,
    #     8: xmas_scan,
    #     9: tcp_window_scan,
    #     10: tcp_maimon_scan,
    #     11: sctp_cookie_echo_scan,
    #     12: tcp_idle_scan,
    #     13: ip_protocol_scan,
    #     14: ping_scan
    # }
    
    print(f"\nScanning IP: {target}\n")
    
    if choice in scan_functions:
        scan = scan_functions[choice]
        run_scan(scan, ports, target, outputs, max_threads=threads)
    
    
if __name__ == "__main__":
    main()