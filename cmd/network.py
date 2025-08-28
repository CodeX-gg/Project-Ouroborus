import os
import sys
import socket
import shutil
import uuid
import requests
import platform
import psutil
import time
import datetime
import subprocess
from colorama import Fore, Style
from .registry import (
    register_command, cwd, HOME, OUTPUT_COLOR, syntax_error, success, section, separator
)

@register_command("whereami", "Show public IP and location.", "System/Network")
def cmd_whereami(args):
    ip = None
    city = region = country = org = lat = lon = None
    try:
        ip = requests.get("https://api.ipify.org").text.strip()
        resp = requests.get(f"https://ipapi.co/{ip}/json/").json()
        city = resp.get('city')
        region = resp.get('region')
        country = resp.get('country_name')
        org = resp.get('org')
        lat = resp.get('latitude')
        lon = resp.get('longitude')
    except:
        pass
    if (not city or city == "?") or (not country or country == "?"):
        try:
            resp2 = requests.get("https://ipinfo.io/json").json()
            city = resp2.get("city", city)
            region = resp2.get("region", region)
            country = resp2.get("country", country)
            org = resp2.get("org", org)
            loc_str = resp2.get("loc", None)
            if loc_str and "," in loc_str:
                lat, lon = loc_str.split(",")
        except:
            pass
    if (not city or city == "?") or (not country or country == "?"):
        try:
            resp3 = requests.get("https://geolocation-db.com/json/").json()
            city = resp3.get('city', city)
            country = resp3.get('country_name', country)
            lat = resp3.get('latitude', lat)
            lon = resp3.get('longitude', lon)
        except:
            pass

    section("Your Location")
    if not ip:
        syntax_error("Could not determine IP.")
        return
    print(f"{Fore.LIGHTYELLOW_EX}IP:{Style.RESET_ALL} {ip}")
    print(f"{Fore.LIGHTYELLOW_EX}City:{Style.RESET_ALL} {city or '?'}")
    print(f"{Fore.LIGHTYELLOW_EX}Region:{Style.RESET_ALL} {region or '?'}")
    print(f"{Fore.LIGHTYELLOW_EX}Country:{Style.RESET_ALL} {country or '?'}")
    print(f"{Fore.LIGHTYELLOW_EX}Org:{Style.RESET_ALL} {org or '?'}")
    if lat and lon:
        print(f"{Fore.LIGHTYELLOW_EX}Latitude:{Style.RESET_ALL} {lat}")
        print(f"{Fore.LIGHTYELLOW_EX}Longitude:{Style.RESET_ALL} {lon}")
        print(f"{Fore.LIGHTCYAN_EX}Map:{Style.RESET_ALL} https://maps.google.com/?q={lat},{lon}")
    else:
        print(f"{Fore.LIGHTRED_EX}Exact coordinates not available.{Style.RESET_ALL}")

@register_command("sysinfo", "Show system statistics.", "System/Network")
def cmd_sysinfo(args):
    import datetime
    section("System Info")
    print(f"{Fore.LIGHTYELLOW_EX}OS:{Style.RESET_ALL} {platform.system()} {platform.release()} {platform.version()}")
    print(f"{Fore.LIGHTYELLOW_EX}Node Name:{Style.RESET_ALL} {platform.node()}")
    print(f"{Fore.LIGHTYELLOW_EX}Processor:{Style.RESET_ALL} {platform.processor()}")
    print(f"{Fore.LIGHTYELLOW_EX}CPU Cores:{Style.RESET_ALL} {psutil.cpu_count(logical=True)}")
    print(f"{Fore.LIGHTYELLOW_EX}RAM:{Style.RESET_ALL} {round(psutil.virtual_memory().total / (1024**3),2)} GB")
    print(f"{Fore.LIGHTYELLOW_EX}Uptime:{Style.RESET_ALL} {str(datetime.timedelta(seconds=int(time.time() - psutil.boot_time())))}")
    print(f"{Fore.LIGHTYELLOW_EX}Python Version:{Style.RESET_ALL} {platform.python_version()}")
    print(f"{Fore.LIGHTYELLOW_EX}MAC Address:{Style.RESET_ALL} {':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])}")

@register_command("cpuinfo", "Show detailed CPU stats.", "System/Network")
def cmd_cpuinfo(args):
    section("CPU Info")
    print(f"{Fore.LIGHTYELLOW_EX}Model:{Style.RESET_ALL} {platform.processor()}")
    print(f"{Fore.LIGHTYELLOW_EX}Cores:{Style.RESET_ALL} {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical")
    print(f"{Fore.LIGHTYELLOW_EX}Usage:{Style.RESET_ALL} {psutil.cpu_percent()}%")
    freqs = psutil.cpu_freq()
    if freqs:
        print(f"{Fore.LIGHTYELLOW_EX}Frequency:{Style.RESET_ALL} {freqs.current} MHz")

@register_command("meminfo", "Show memory usage.", "System/Network")
def cmd_meminfo(args):
    section("Memory Info")
    vm = psutil.virtual_memory()
    print(f"{Fore.LIGHTYELLOW_EX}Total:{Style.RESET_ALL} {round(vm.total/(1024**3),2)} GB")
    print(f"{Fore.LIGHTYELLOW_EX}Available:{Style.RESET_ALL} {round(vm.available/(1024**3),2)} GB")
    print(f"{Fore.LIGHTYELLOW_EX}Used:{Style.RESET_ALL} {round(vm.used/(1024**3),2)} GB")
    print(f"{Fore.LIGHTYELLOW_EX}Percent:{Style.RESET_ALL} {vm.percent}%")

@register_command("diskinfo", "Show disk usage for this drive.", "System/Network")
def cmd_diskinfo(args):
    section("Disk Info")
    usage = psutil.disk_usage(cwd)
    print(f"{Fore.LIGHTYELLOW_EX}Total:{Style.RESET_ALL} {round(usage.total/(1024**3),2)} GB")
    print(f"{Fore.LIGHTYELLOW_EX}Used:{Style.RESET_ALL} {round(usage.used/(1024**3),2)} GB")
    print(f"{Fore.LIGHTYELLOW_EX}Free:{Style.RESET_ALL} {round(usage.free/(1024**3),2)} GB")
    print(f"{Fore.LIGHTYELLOW_EX}Percent:{Style.RESET_ALL} {usage.percent}%")

@register_command("netinfo", "Show network interfaces and IPs.", "System/Network")
def cmd_netinfo(args):
    section("Network Interfaces")
    addrs = psutil.net_if_addrs()
    for iface, addrlist in addrs.items():
        print(f"{Fore.LIGHTBLUE_EX}{iface}{Style.RESET_ALL}: ", end="")
        for addr in addrlist:
            if addr.family == socket.AF_INET:
                print(f"{Fore.LIGHTYELLOW_EX}IP:{Style.RESET_ALL} {addr.address} ", end="")
            elif addr.family == socket.AF_INET6:
                print(f"{Fore.LIGHTMAGENTA_EX}IPv6:{Style.RESET_ALL} {addr.address} ", end="")
            elif addr.family == psutil.AF_LINK:
                print(f"{Fore.LIGHTGREEN_EX}MAC:{Style.RESET_ALL} {addr.address} ", end="")
        print()
    separator()

@register_command("mac", "Show this device's MAC address.", "System/Network")
def cmd_mac(args):
    print(f"{Fore.LIGHTYELLOW_EX}MAC Address:{Style.RESET_ALL} {':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])}")

@register_command("whoami", "Show user information.", "System/Network")
def cmd_whoami(args):
    from .registry import USER, HOME
    section("User Info")
    print(f"{Fore.LIGHTYELLOW_EX}Username:{Style.RESET_ALL} {USER}")
    print(f"{Fore.LIGHTYELLOW_EX}Home:{Style.RESET_ALL} {HOME}")

@register_command("datetime", "Show current date and time.", "System/Network")
def cmd_datetime(args):
    now = datetime.datetime.now()
    print(f"{Fore.LIGHTYELLOW_EX}Local:{Style.RESET_ALL} {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Fore.LIGHTYELLOW_EX}UTC:{Style.RESET_ALL} {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")

@register_command("uptime", "Show system uptime.", "System/Network")
def cmd_uptime(args):
    uptime = time.time() - psutil.boot_time()
    print(f"{Fore.LIGHTYELLOW_EX}System Uptime:{Style.RESET_ALL} {str(datetime.timedelta(seconds=int(uptime)))}")

@register_command("ping", "Ping a host.", "System/Network")
def cmd_ping(args):
    host = input("Host: ")
    count = 4
    cmd = f"ping -n {count} {host}" if os.name == "nt" else f"ping -c {count} {host}"
    print(f"Pinging {host}...")
    os.system(cmd)

@register_command("ps", "List running processes.", "System/Network")
def cmd_ps(args):
    section("Processes")
    for p in psutil.process_iter(['pid', 'name', 'username']):
        print(f"{Fore.LIGHTYELLOW_EX}{p.info['pid']:>6}{Style.RESET_ALL}  {p.info['name'][:22]:22}  {p.info['username']}")

@register_command("portscan", "Scan open TCP ports on a host.", "System/Network")
def cmd_portscan(args):
    host = input("Host: ")
    start = int(input("Start port: "))
    end = int(input("End port: "))
    section(f"Scanning {host} ports {start}-{end}")
    open_ports = []
    for port in range(start, end+1):
        try:
            with socket.create_connection((host, port), timeout=0.2):
                open_ports.append(port)
        except:
            pass
    if open_ports:
        print(f"{Fore.LIGHTYELLOW_EX}Open ports:{Style.RESET_ALL} {open_ports}")
    else:
        print(f"{Fore.LIGHTRED_EX}No open ports found.{Style.RESET_ALL}")

@register_command("dnslookup", "DNS lookup for a host or IP.", "System/Network")
def cmd_dnslookup(args):
    q = input("Enter host or IP to lookup: ")
    try:
        res = socket.gethostbyname_ex(q)
        print(f"{Fore.LIGHTYELLOW_EX}DNS Result:{Style.RESET_ALL} {res}")
    except Exception as e:
        syntax_error(e)

@register_command("traceroute", "Perform a traceroute to a host.", "System/Network")
def cmd_traceroute(args):
    host = input("Host to traceroute: ")
    section(f"Traceroute to {host}")
    cmd = ["tracert", host] if os.name == "nt" else ["traceroute", host]
    try:
        out = subprocess.check_output(cmd).decode(errors='replace')
        print(f"{Fore.LIGHTYELLOW_EX}{out}{Style.RESET_ALL}")
    except Exception as e:
        syntax_error(e)

@register_command("speedtest", "Run an internet speed test.", "System/Network")
def cmd_speedtest(args):
    section("Speedtest")
    try:
        import speedtest
        st = speedtest.Speedtest()
        st.get_best_server()
        st.download()
        st.upload()
        res = st.results.dict()
        print(f"{Fore.LIGHTYELLOW_EX}Ping:{Style.RESET_ALL} {res['ping']:.2f} ms")
        print(f"{Fore.LIGHTYELLOW_EX}Download:{Style.RESET_ALL} {res['download'] / 1e6:.2f} Mbps")
        print(f"{Fore.LIGHTYELLOW_EX}Upload:{Style.RESET_ALL} {res['upload'] / 1e6:.2f} Mbps")
        print(f"{Fore.LIGHTYELLOW_EX}ISP:{Style.RESET_ALL} {res['client']['isp']}")
    except Exception as e:
        syntax_error(e)

@register_command("network", "Show bandwidth usage and interfaces.", "System/Network")
def cmd_network(args):
    section("Network Stats")
    try:
        interfaces = psutil.net_if_addrs()
        for iface, info in interfaces.items():
            print(f"{Fore.LIGHTBLUE_EX}{iface}{Style.RESET_ALL}:")
            for addr in info:
                print(f"  {addr.family}: {addr.address}")
        io_counters = psutil.net_io_counters()
        print(f"{Fore.LIGHTYELLOW_EX}Bandwidth sent:{Style.RESET_ALL} {io_counters.bytes_sent} bytes")
        print(f"{Fore.LIGHTYELLOW_EX}Bandwidth recv:{Style.RESET_ALL} {io_counters.bytes_recv} bytes")
    except Exception as e:
        syntax_error(e)
    print("Latency to 8.8.8.8 (ms): ", end="")
    if shutil.which("ping"):
        try:
            latency = subprocess.check_output("ping -c 1 8.8.8.8", shell=True).decode()
            print(latency.split("time=")[1].split(" ms")[0])
        except:
            print("N/A")
    else:
        print("Ping not available")

@register_command("broadcast", "Show broadcast addresses for all interfaces.", "System/Network")
def cmd_broadcast(args):
    try:
        for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if hasattr(addr, 'broadcast') and addr.broadcast:
                    print(f"{Fore.LIGHTYELLOW_EX}{iface} broadcast:{Style.RESET_ALL} {addr.broadcast}")
    except Exception as e:
        syntax_error(e)

@register_command("publicip", "Show your public IP address.", "System/Network")
def cmd_publicip(args):
    try:
        ip = requests.get("https://api.ipify.org").text.strip()
        print(f"{Fore.LIGHTYELLOW_EX}Public IP:{Style.RESET_ALL} {ip}")
    except Exception as e:
        syntax_error(e)

@register_command("localip", "Show all local IP addresses.", "System/Network")
def cmd_localip(args):
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                print(f"{Fore.LIGHTYELLOW_EX}{iface}:{Style.RESET_ALL} {addr.address}")

@register_command("wakeonlan", "Send a Wake-on-LAN magic packet.", "System/Network")
def cmd_wakeonlan(args):
    mac = input("MAC address (format: 01:23:45:67:89:ab): ").strip()
    try:
        addr = bytes.fromhex(mac.replace(':', ''))
        packet = b'\xff' * 6 + addr * 16
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(packet, ('<broadcast>', 9))
        s.close()
        success(f"Magic packet sent to {mac}")
    except Exception as e:
        syntax_error(e)

@register_command("openports", "Show all open TCP ports on localhost.", "System/Network")
def cmd_openports(args):
    section("Open TCP Ports")
    try:
        for conn in psutil.net_connections(kind='tcp'):
            if conn.status == 'LISTEN':
                print(f"{Fore.LIGHTYELLOW_EX}Port:{Style.RESET_ALL} {conn.laddr.port} (PID: {conn.pid})")
    except Exception as e:
        syntax_error(e)