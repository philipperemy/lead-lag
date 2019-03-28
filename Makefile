all:
	make install

install:
	pip install cython
	pip install . --upgrade
	python setup.py build_ext --inplace

uninstall:
	pip uninstall lead-lag

clean:
	rm -rf *.out *.c *.bin *.exe *.o *.a *.so build *.html __pycache__
