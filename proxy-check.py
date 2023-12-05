import requests
import socks
import socket
from urllib.parse import urlparse
from tqdm import tqdm  # Import tqdm for the progress bar

def fetch_proxy_list(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.text.split('\n')
    else:
        raise Exception(f"Failed to fetch proxy list. Status code: {response.status_code}")

def test_http_proxy(proxy, timeout=5):
    try:
        # Split the IP and Port
        ip, port = proxy.split(':')
        proxies = {'http': f'http://{ip}:{port}', 'https': f'https://{ip}:{port}'}
        response = requests.get("http://www.google.com", proxies=proxies, timeout=timeout)
        return response.status_code == 200
    except requests.Timeout:
        return False
    except requests.RequestException:
        return False

def test_socks_proxy(proxy, timeout=5):
    try:
        # Split the IP and Port
        ip, port = proxy.split(':')
        parsed_url = urlparse(proxy)
        socks.set_default_proxy(socks.SOCKS5, ip, int(port))
        socket_instance = socks.socksocket()
        socket_instance.settimeout(timeout)  # Set timeout for the socket
        socket_instance.connect(("www.google.com", 80))
        return True
    except (socket.error, socks.ProxyConnectionError, socket.timeout):
        return False
    finally:
        socket_instance.close()

def save_working_proxies(proxies, proxy_type):
    filename = f"working_{proxy_type}_proxies.txt"
    with open(filename, 'w') as file:
        for proxy in tqdm(proxies, desc=f"Saving {proxy_type} proxies", unit=" proxies"):
            if proxy_type == 'http' and test_http_proxy(proxy):
                file.write(f"{proxy}\n")
            elif proxy_type == 'socks' and test_socks_proxy(proxy):
                file.write(f"{proxy}\n")
    print(f"Saved working {proxy_type} proxies to {filename}")

def main():
    proxy_api_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    
    try:
        proxy_list = fetch_proxy_list(proxy_api_url)

        http_proxies = []
        socks_proxies = []
        http_proxies_found = 0  # Counter for working HTTP proxies
        for proxy in tqdm(proxy_list, desc="Checking proxies", unit=" proxies"):
            proxy = proxy.strip()
            ip, port = proxy.split(':')
            if test_http_proxy(proxy, timeout=0.4):  # Set your desired timeout value (in seconds)
                print(f"\nHTTP Proxy {proxy} is working.")
                http_proxies.append(proxy)
                http_proxies_found += 1
                if http_proxies_found == 5:
                    print("Found 5 working HTTP proxies. Exiting...")
                    break
            else:
                print(f"\nHTTP Proxy {proxy} is not working.")
            
            if test_socks_proxy(proxy, timeout=0.4):  # Set your desired timeout value (in seconds)
                print(f"SOCKS Proxy {proxy} is working.")
                socks_proxies.append(proxy)
            else:
                print(f"SOCKS Proxy {proxy} is not working.")
        
        save_working_proxies(http_proxies, 'http')
        save_working_proxies(socks_proxies, 'socks')

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
