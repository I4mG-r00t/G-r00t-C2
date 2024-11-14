#include <stdio.h>

int main(int argc, char *argv[]) {
    printf("Test program started.\n");

    if (argc != 3) {
        printf("Usage: test <IP> <PORT>\n");
    } else {
        printf("IP: %s, PORT: %s\n", argv[1], argv[2]);
    }
    return 0;
}