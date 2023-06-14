CC = g++
CFLAGS = -std=c++11 -Wall -Wextra
LDFLAGS = `pkg-config opencv4 --cflags --libs`
SRC = imagenC.cpp
TARGET = programa

all: $(TARGET)

$(TARGET): imagenC.cpp
	$(CC) $(CFLAGS) -o $(TARGET) imagenC.cpp $(LDFLAGS)

clean:
	rm -f $(TARGET)