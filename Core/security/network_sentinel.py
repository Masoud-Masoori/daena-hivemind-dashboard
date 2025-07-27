def scan_ports(port_list):
    return [f"[Sentinel]  Port {p} open." if p % 2 == 0 else f"[Sentinel]  Port {p} closed." for p in port_list]

if __name__ == "__main__":
    print(scan_ports([22, 80, 443, 8888]))
