all:
	make install

install:
	pip install cython
	python setup.py build_ext --inplace
	pip install . --upgrade

uninstall:
	pip uninstall lead-lag

clean:
	rm -rf *.out *.c *.bin *.exe *.o *.a *.so build *.html __pycache__
