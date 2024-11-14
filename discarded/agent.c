#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <unistd.h>

// Custom implementation of strndup for Windows
char* strndup(const char *src, size_t n) {
    size_t len = strnlen(src, n);
    char *dst = (char *)malloc(len + 1);
    if (dst) {
        memcpy(dst, src, len);
        dst[len] = '\0';
    }
    return dst;
}

void print_usage() {
    printf("Usage: agent <SERVER_IP> <SERVER_PORT>\n");
}

// Callback function to capture the response
static size_t write_callback(void *contents, size_t size, size_t nmemb, void *userp) {
    printf("Data received: %s\n", (char *)contents); // Debug output
    size_t realsize = size * nmemb;
    char **response_ptr = (char **)userp;
    *response_ptr = strndup(contents, realsize); // Using custom strndup
    return realsize;
}

// Main function
int main(int argc, char *argv[]) {
    if (argc != 3) {
        print_usage();
        return 1;
    }

    const char* server_ip = argv[1];
    const char* server_port = argv[2];
    char url[256];
    snprintf(url, sizeof(url), "http://%s:%s/command", server_ip, server_port);
    printf("Connecting to URL: %s\n", url); // Debug output

    CURL *curl;
    CURLcode res;
    char *response = NULL;

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

        res = curl_easy_perform(curl);

        if(res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        } else {
            printf("Command received: %s\n", response);
        }

        curl_easy_cleanup(curl);
    } else {
        fprintf(stderr, "CURL initialization failed\n");
    }

    curl_global_cleanup();
    free(response);
    return 0;
}
