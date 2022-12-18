#include <iostream>
#include <cstring>
#include <arpa/inet.h>

using std::cout, std::cin, std::endl, std::string, std::hex, std::stoi;

bool wakeOnLan(string MAC_adress) {
    struct sockaddr_in udpClient, udpServer;
    int udpSocket = socket(AF_INET, SOCK_DGRAM, 0);
    int broadcast = 1 ;
    int MAC_array[6];
    unsigned char packet[102];

    if (setsockopt(udpSocket, SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof broadcast) == -1) {
        perror("setsockopt (SO_BROADCAST)");
        exit(EXIT_FAILURE);
    }

    udpClient.sin_family = AF_INET;
    udpClient.sin_addr.s_addr = INADDR_ANY;
    udpClient.sin_port = 0;

    udpServer.sin_family = AF_INET;
    udpServer.sin_addr.s_addr = inet_addr("255.255.255.255");
    udpServer.sin_port = htons(9); // used port

    bind(udpSocket, (struct sockaddr*)&udpClient, sizeof(udpClient));

    for (int i = 0; i < 6; i++) {
        int limiter = MAC_adress.find(':');
        string temp;
        temp = MAC_adress.substr(0, limiter);
        MAC_adress.erase(0, limiter+1);
        MAC_array[i] = stoi(temp, 0, 16);
    }

    for (int i = 0; i < 6; i++) {
        packet[i] = 0xFF;
    }
    for (int i = 6; i < 102; i++) {
        packet[i] = MAC_array[i % 6];
    }

    sendto(udpSocket, &packet, sizeof(unsigned char) * 102, 0, (struct sockaddr*)&udpServer, sizeof(udpServer));

    return true;
}
int main() {
// b4:2e:99:1c:28:e4 pc 192.168.0.103
// 00:21:cc:c4:88:63 laptop 192.168.0.104

    string MAC_adresses[] = {"00:21:CC:C4:88:63", "b4:2e:99:1c:28:e4"};

    for (string MAC_adress : MAC_adresses) {
        if (wakeOnLan(MAC_adress)) {
            cout << "Magic packet send to "<< MAC_adress << endl;
        }
    }
    return 0;
}

