import dns.resolver
import sys

subdomains = [
    "www","mail","ftp","dev","test","api","blog","admin","vpn","ns1","ns2"
]

def get_records(domain):
    print("\n[+] DNS Records\n")

    records = ["A","AAAA","MX","NS","TXT","CNAME"]

    for record in records:
        try:
            answers = dns.resolver.resolve(domain, record)
            for rdata in answers:
                print(f"{record}: {rdata}")
        except:
            pass


def brute_subdomains(domain):
    print("\n[+] Subdomain Scan\n")

    for sub in subdomains:
        target = f"{sub}.{domain}"

        try:
            dns.resolver.resolve(target,"A")
            print(f"Found: {target}")
        except:
            pass


def main():

    if len(sys.argv) != 2:
        print("Usage: python dns_recon.py domain.com")
        return

    domain = sys.argv[1]

    print(f"\nScanning: {domain}")

    get_records(domain)
    brute_subdomains(domain)


if __name__ == "__main__":
    main()
