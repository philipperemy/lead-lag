all:
	make install

install:
	pip install cython
	pip install . --upgrade

uninstall:
	pip uninstall lead-lag

clean:
	rm -rf *.out *.c *.bin *.exe *.o *.a *.so build *.html __pycache__
