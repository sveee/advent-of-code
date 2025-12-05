
DAY ?= $(shell date +%d)
DAY_VALUE = $(shell printf "%02d" $(DAY))

SRC = $(DAY_VALUE).cpp
BIN = bin/$(DAY_VALUE)

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