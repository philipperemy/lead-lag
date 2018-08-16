all:
	python setup.py build_ext --inplace
clean:
	rm -rf *.out *.c *.bin *.exe *.o *.a *.so test build *.html
