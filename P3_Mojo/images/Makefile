CC = g++
CFLAGS = -std=c++11 -Wall -Wextra
LDFLAGS = `pkg-config opencv4 --cflags --libs`
SRC = imagenC.cpp
TARGET = programa

all: $(TARGET)

$(TARGET): imagenC.cpp
	$(CC) $(CFLAGS) -o $(TARGET) imagenC.cpp $(LDFLAGS)
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/

clean:
	rm -f $(TARGET)