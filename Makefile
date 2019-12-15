all:
	make install

install:
	pip install cython
	python setup.py build_ext --inplace
	pip install . --upgrade

uninstall:
	pip uninstall -y lead-lag

clean:
	rm -rf *.out lead_lag/*.c *.bin *.exe *.o *.a lead_lag/*.so build *.html __pycache__ lead_lag/__pycache__ notebooks/.ipynb_checkpoints/
