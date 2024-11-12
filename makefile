# Makefile for building the agent and server
CC = gcc
CFLAGS = -lcurl
TARGET = agent

all: $(TARGET)

$(TARGET): agent.c
	$(CC) agent.c -o $(TARGET) $(CFLAGS)

clean:
	rm -f $(TARGET)
