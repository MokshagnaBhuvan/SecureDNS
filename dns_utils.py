import requests
import subprocess
import dns.resolver
import dns.reversename

def get_ip_addresses_from_google(domain):
    url = f"https://dns.google/resolve?name={domain}&type=A"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        ip_addresses = [answer['data'] for answer in data.get('Answer', []) if answer['type'] == 1]
        return sorted(ip_addresses)
    except Exception as e:
        print(f"❌ Error fetching IP addresses for {domain}: {e}")
        return []

def get_ip_addresses_from_cloudflare(domain):
    url = f"https://cloudflare-dns.com/dns-query?name={domain}&type=A"
    headers = {"Accept": "application/dns-json"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        ip_addresses = [answer['data'] for answer in data.get('Answer', []) if answer['type'] == 1]
        return sorted(ip_addresses)
    except Exception as e:
        print(f"❌ Error fetching IP addresses for {domain} from Cloudflare: {e}")
        return []

def forward_dns_query(domain):
    records = {
        "A": None,
        "AAAA": None, #apply recursive ip check for domains on AAAA and A records
        "CNAME": None,
        "MX": None,
        "TXT": None,
        "NS": None,
        "SOA": None
    }
    
    try:
        records["A"] = [str(r) for r in dns.resolver.resolve(domain, 'A')]
    except:
        pass
    
    try:
        records["AAAA"] = [str(r) for r in dns.resolver.resolve(domain, 'AAAA')]
    except:
        pass
    
    try:
        records["CNAME"] = [str(r) for r in dns.resolver.resolve(domain, 'CNAME')]
    except:
        pass
    
    try:
        records["MX"] = [str(r) for r in dns.resolver.resolve(domain, 'MX')]
    except:
        pass
    
    try:
        records["TXT"] = [str(r) for r in dns.resolver.resolve(domain, 'TXT')]
    except:
        pass
    
    try:
        records["NS"] = [str(r) for r in dns.resolver.resolve(domain, 'NS')]
    except:
        pass
    
    try:
        records["SOA"] = [str(r) for r in dns.resolver.resolve(domain, 'SOA')]
    except:
        pass
    
    return records

if __name__ == "__main__":
    # domain = input("Enter the domain: ")
    # result = forward_dns_query(domain)
    # for record_type, values in result.items():
    #     print(f"{record_type} : {values if values else 'No record found'}")
    print("This script is not meant to be run directly.")
    print("Please run main.py to start the DNS middleware.")