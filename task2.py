import time
import re
from hyperloglog import HyperLogLog

def load_ip_addresses(filepath):
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    with open(filepath, "r") as file:
        for line in file:
            match = ip_pattern.search(line)
            if match:
                yield match.group()

def exact_count(ips):
    unique_ips = set()
    for ip in ips:
        unique_ips.add(ip)
    return len(unique_ips)

def hll_count(ips, error_rate=0.01):
    hll = HyperLogLog(error_rate)
    for ip in ips:
        hll.add(ip)
    return len(hll)

if __name__ == "__main__":
    filepath = "lms-stage-access.log"
    ips = list(load_ip_addresses(filepath))

    start = time.time()
    exact_result = exact_count(ips)
    exact_time = time.time() - start

    start = time.time()
    approx_result = hll_count(ips)
    hll_time = time.time() - start

    print("Результати порівняння:")
    print(f"{'':<25}{'Точний підрахунок':<20}{'HyperLogLog'}")
    print(f"{'Унікальні елементи':<25}{exact_result:<20}{approx_result}")
    print(f"{'Час виконання (сек.)':<25}{round(exact_time, 5):<20}{round(hll_time, 5)}")
