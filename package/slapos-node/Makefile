#!/usr/bin/make -f
# -*- makefile -*-

build: 
	cd slapprepare; python setup.py build
	cd slapos; make build

all: build

install: all
#	cd slapprepare; python setup.py install
	cd slapos; make install
        mkdir -p $(DESTDIR)/usr/sbin/
        cp slapos-start $(DESTDIR)/usr/sbin/

clean:
	cd slapprepare; python setup.py clean
#	cd slapos; make clean

# Début 23:39