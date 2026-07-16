CC ?= gcc
CFLAGS ?= -fPIC -Wall -O3 -ffast-math -fomit-frame-pointer
#CFLAGS ?= -g -O0 -DDRAGON_DEBUG -Wall

ifeq (${DRAGON_INCLUDE_DIR},)
    L_DRAGON_INCLUDE_DIR = $(shell dragon-config -o)
else
	L_DRAGON_INCLUDE_DIR = -I ${DRAGON_INCLUDE_DIR}
endif

ifeq (${DRAGON_LIB_DIR},)
    L_DRAGON_LIB_DIR = $(shell  dragon-config -l)
else
	L_DRAGON_LIB_DIR = -L ${DRAGON_LIB_DIR} -l dragon
endif

ifeq ($(VIRTUAL_ENV),)
	VIRTUAL_ENV = $(CONDA_PREFIX)
endif

INCLUDE = $(L_DRAGON_INCLUDE_DIR) -I ${VIRTUAL_ENV}/include
LIBS = $(L_DRAGON_LIB_DIR)

BIN_FILES = worker

%.c.o: %.c
	$(CC) $(INCLUDE) $(CFLAGS) -c $< -o $@

default: build

build: worker

worker: worker.cpp
	g++ $(INCLUDE) -std=c++14 -o worker $< $(LIBS) -ldl

clean:
	rm -rf *.o $(BIN_FILES) core __pycache__