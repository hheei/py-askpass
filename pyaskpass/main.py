import re
import sys
import pyotp
from pathlib import Path

def parse_ssh_config():
    def search(pattern, text):
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        return None
    
    cfg = Path("~/.ssh/config").expanduser().read_text()
    hosts = {}
    matches = list(re.finditer(r"Host\s+(.*)", cfg))
    for i, match in enumerate(matches):
        host = match.group(1)
        host_info = cfg[match.end() + 1:matches[i+1].start() - 1 if i+1 < len(matches) else None]
        password = search(r"#Password\s+(.*)", host_info)
        totp = search(r"#TOTP\s+(.*)", host_info)

        hosts[host] = {
            "password": password or "",
            "totp": totp or ""
        }
    
    return hosts

def main():
    ssh_cfg = parse_ssh_config()
    args = tuple(sys.argv[1:])
    for host in ssh_cfg:
        if host in args:
            if ssh_cfg[host]['totp']:
                totp = pyotp.TOTP(ssh_cfg[host]['totp']).now()
            else:
                totp = ""
            print(f"{ssh_cfg[host]['password']},{totp}")
            break
    return 0

if __name__ == "__main__":
    main()