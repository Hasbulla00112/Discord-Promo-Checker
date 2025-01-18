import threading
import httpx
import itertools
from colorama import Fore, Style, init
import os
import time

init(autoreset=True)

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    
    def increment(self):
        with self.lock:
            self.value += 1
            return self.value

def create_output_dir():
    timestamp = time.strftime('%Y-%m-%d %H-%M-%S')
    output_dir = f'output/{timestamp}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def printSuccess(text):
    print(f"{Style.BRIGHT}{Fore.GREEN}{text}")

def printError(text):
    print(f"{Style.BRIGHT}{Fore.RED}{text}")

def printInfo(text):
    print(f"{Style.BRIGHT}{Fore.CYAN}{text}")

# Read proxies and create cycle
proxies = itertools.cycle(open("input/proxies.txt", "r").read().splitlines())

# Read and deduplicate links without cycling
with open("input/promos.txt", "r") as f:
    links = [ii for n, ii in enumerate(f.read().splitlines()) if ii not in f.read().splitlines()[:n]]

counter = Counter()
total_links = len(links)
to_check = list(range(total_links))
to_check_lock = threading.Lock()
output_dir = None  # Will be set in main

def checkCode(code, proxy):
    client = httpx.Client(transport=httpx.HTTPTransport(proxy=f"http://{proxy}"))
    try:
        res = client.get("https://discord.com/api/v9/entitlements/gift-codes/" + code + "?country_code=ES&with_application=false&with_subscription_plan=true")
        if res.status_code == 200:
            json_data = res.json()
            if not json_data['redeemed'] and json_data['max_uses'] != json_data['uses']:
                expiration = str(json_data['promotion']['inbound_header_text']).split('T')[0]
                return expiration
        return "nope"
    finally:
        client.close()

def get_code_from_input(input_text):
    """Extract code from either full URL or direct code"""
    input_text = input_text.strip()
    if "discord.gg" in input_text:
        return input_text.split("discord.gg/")[1]
    if "promos.discord.gg" in input_text:
        return input_text.split("promos.discord.gg/")[1]
    return input_text

def checkLoop():
    while True:
        try:
            # Get next index to check in a thread-safe way
            with to_check_lock:
                if not to_check:
                    break
                current_index = to_check.pop(0)
            
            link = links[current_index]
            proxy = next(proxies)

            code = get_code_from_input(link)
            res = checkCode(code, proxy)
            
            # Increment counter in a thread-safe way
            current_count = counter.increment()

            if res == "nope":
                printError(f"Invalid [{code}] ({current_count}/{total_links})")
            else:
                printSuccess(f"Valid [{res}] [{code}] ({current_count}/{total_links})")
                with open(f"{output_dir}/valid.txt", "a") as f:
                    f.write(f"{link} | {res}\n")
        except Exception as e:
            printError(f"Got an error: {str(e)}")

if __name__ == "__main__":
    if not os.path.exists("output"):
        os.makedirs("output")
        
    if not os.path.exists("input/proxies.txt"):
        printError("Missing proxies file: input/proxies.txt")
        exit(1)
        
    if not os.path.exists("input/promos.txt"):
        printError("Missing links file: input/promos.txt")
        exit(1)
    
    # Create timestamped output directory
    output_dir = create_output_dir()
    
    # Create empty valid.txt in the timestamped directory
    with open(f"{output_dir}/valid.txt", "w") as f:
        f.write("")
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    printInfo(f"Loaded {total_links} unique links to check")
    thread_count = int(input("Thread count: "))
    
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=checkLoop)
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
        
    printInfo("Checking completed!")