import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def load_proxies(file_path):
    """
    Load proxy addresses from the specified file.
    """
    proxies = []
    with open(file_path, 'r') as f:
        for line in f:
            proxy = line.strip()
            if proxy:
                proxies.append(proxy)
    return proxies


def test_proxy(proxy, test_url='http://www.google.com', timeout=2):
    """
    Test a single proxy by attempting a GET request to test_url.
    Returns a tuple of (proxy, status, response_time).
    """
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}',
    }
    try:
        response = requests.get(test_url, proxies=proxies, timeout=timeout)
        if response.status_code == 200:
            return proxy, True, response.elapsed.total_seconds()
        else:
            return proxy, False, None
    except Exception:
        return proxy, False, None


def main():
    # Load proxies from file
    proxies = load_proxies('proxies.txt')
    working_proxies = []

    # Use a thread pool to test proxies concurrently
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_proxy = {executor.submit(test_proxy, proxy): proxy for proxy in proxies}

        # Process results as they complete
        for future in as_completed(future_to_proxy):
            proxy, status, _ = future.result()
            if status:
                # Only output (print) proxies that are working
                print(proxy)
                working_proxies.append(proxy)

    # Write only the working proxies to checked_proxies.txt
    with open('checked_proxies.txt', 'w') as f:
        for proxy in working_proxies:
            f.write(f"{proxy}\n")


if __name__ == '__main__':
    main()
