
DAY ?= $(shell date +%d)

SRC = $(DAY).cpp
BIN = bin/$(DAY)

CXX = g++
CXXFLAGS = --std=c++23 -O3

.PHONY: all format clean

all: $(BIN)

$(BIN): $(SRC) | bin
	$(CXX) $(CXXFLAGS) $(SRC) -o $(BIN)

bin:
	@mkdir -p bin

format:
	clang-format -i $(SRC)

clean:
	@echo "Cleaning up binaries..."
	rm -rf bin