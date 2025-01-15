#!/bin/python3

import sys
import socket
from datetime import datetime
import threading
from queue import Queue
from colorama import Fore, Back, Style, init

init(autoreset=True)
print_lock = threading.Lock()
port_queue = Queue()

def scan_port(target):
    while True:  
        port = port_queue.get()
        
        if port is None:
            break
            
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = s.connect_ex((target, port))
            if result == 0:
            	with print_lock:
                    print(f"{Fore.GREEN}[+] Port {port} is open{Style.RESET_ALL}")
            s.close()
        except:
            pass
        
        port_queue.task_done()

def main():
    # Defining target
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Invalid amount of arguments")
        print(f"{Fore.YELLOW}Syntax: python3 portScanner.py <ip>{Style.RESET_ALL}")
        sys.exit()

    # translate hostname to IPv4
    target = socket.gethostbyname(sys.argv[1])

    # Adding pretty banner
    banner = fr"""{Fore.CYAN}
                  _                                         
 _ __   ___  _ __| |_   ___  ___ __ _ _ __  _ __   ___ _ __ 
| '_ \ / _ \| '__| __| / __|/ __/ _` | '_ \| '_ \ / _ \ '__|
| |_) | (_) | |  | |_  \__ \ (_| (_| | | | | | | |  __/ |   
| .__/ \___/|_|   \__| |___/\___\__,_|_| |_|_| |_|\___|_|   
|_|
{Style.RESET_ALL}
{Fore.RED}[*] Created By: Can Simsek
"""
    print(banner)
    print(f"{Fore.YELLOW}{'*' * 50}")
    print(f"{Fore.BLUE}Scanning target: {Fore.WHITE}{target}")
    print(f"{Fore.BLUE}Time started: {Fore.WHITE}{str(datetime.now())}")
    print(f"{Fore.YELLOW}{'*' * 50}{Style.RESET_ALL}")

    try:
        thread_count = 100  # thread counts
        threads = []  # empty thread list
        
        # create threads and start them
        for i in range(thread_count):
            thread = threading.Thread(target=scan_port, args=(target,))
            thread.start()
            threads.append(thread)
        
        # put the ports into queue        
        for port in range(1, 1001):
            port_queue.put(port)

        # wait until threads terminated
        port_queue.join()
        
        # terminate the threads
        for i in range(thread_count):
            port_queue.put(None)
        for t in threads:
            t.join()

    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Exiting program.{Style.RESET_ALL}")
        sys.exit()
    except socket.gaierror:
        print(f"{Fore.RED}Hostname could not be resolved.{Style.RESET_ALL}")
        sys.exit()
    except socket.error:
        print(f"{Fore.RED}Could not connect to server.{Style.RESET_ALL}")
        sys.exit()

if __name__ == "__main__":
    main()
